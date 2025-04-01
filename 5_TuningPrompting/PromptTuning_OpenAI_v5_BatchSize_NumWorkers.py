# @title OPENAI
import json
import pandas as pd
import time
import openai
from openai import OpenAIError
from dotenv import load_dotenv
import os
from pathlib import Path
import argparse
import logging
import re
import concurrent.futures
from typing import List, Dict
import math
from openpyxl import load_workbook
import psutil
import multiprocessing
import threading

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# Replace 'your_api_key_here' with your actual OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
print(openai.api_key[:10])
# @title OPENAI KO CÓ MESSAGE HISTORY
def process_conversation(order, base_prompt, inputs, conversation_history=None):
    print(f"\n=== Processing Conversation ===")
    print(f"Order: {order}")
    print(f"Base Prompt: {base_prompt[:100]}...")
    
    # Log conversation history
    if conversation_history:
        logger.info(f"Conversation history: {conversation_history}")

    # Tạo model config dưới dạng JSON
    model_config = {
        "model": "gpt-4o",
        "temperature": 0.3,
        "max_tokens": 4096,
        "top_p": 1,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }
    model_config_json = json.dumps(model_config)
    
    responses = []
    response_times = []
    chat_messages = []
    
    # 1. System message
    chat_messages.append({"role": "system", "content": base_prompt})
    print("\nSau khi thêm system message:")
    print(chat_messages)
    
    # 2. History handling
    if conversation_history and not pd.isna(conversation_history):
        try:
            # Parse conversation history from JSON string
            history_messages = json.loads(conversation_history)
            
            # Validate format of history messages
            if isinstance(history_messages, list):
                for msg in history_messages:
                    if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                        chat_messages.append(msg)
                    else:
                        print(f"Warning: Skipping invalid message format in history: {msg}")
            else:
                print(f"Warning: conversation_history is not a list: {history_messages}")
            
            print("\nSau khi thêm history:")
            print(json.dumps(chat_messages, indent=2, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            print(f"Error parsing conversation history: {e}")
            print(f"Raw conversation history: {conversation_history}")
            logger.error(f"Error parsing conversation history: {e}")
            logger.error(f"Raw conversation history: {conversation_history}")
    
    # 3. New input
    for user_input in inputs:
        chat_messages.append({"role": "user", "content": user_input})
        print("\nTrước khi gọi API:")
        print(json.dumps(chat_messages, indent=2, ensure_ascii=False))
        
        start_time = time.time()
        try_count = 0
        while try_count < 3:
            try:
                print(f"DEBUG - Attempt {try_count + 1} to call OpenAI API")
                completion = openai.chat.completions.create(
                    model=model_config["model"],
                    messages=chat_messages,   
                    temperature=model_config["temperature"],
                    max_tokens=model_config["max_tokens"],
                    top_p=model_config["top_p"],
                    frequency_penalty=model_config["frequency_penalty"],
                    presence_penalty=model_config["presence_penalty"]
                )
                end_time = time.time()
                response_content = completion.choices[0].message.content
                chat_messages.append({"role": "assistant", "content": response_content})

                responses.append(response_content)
                response_times.append(end_time - start_time)

                # Print the completion output here
                print(f"Order {order}, Input: '{user_input}', Response: '{response_content}', Time: {end_time - start_time:.2f}s\n====")
                print(f"DEBUG - Chat messages after AI response: {chat_messages}")
                break
            except OpenAIError as e:
                try_count += 1
                print(f"DEBUG - API Error on attempt {try_count}: {str(e)}")
                if try_count >= 3:
                    responses.append("Request failed after 2 retries.")
                    response_times.append("-")
                    print(f"Order {order}, Input: '{user_input}', Response: 'Request failed after 2 retries.', Time: -")
                else:
                    print(f"DEBUG - Waiting 3 seconds before retry...")
                    time.sleep(3)

    # Reset the message history for the next order
    return  responses, response_times, chat_messages, model_config_json

sheet_name = 'Trang tính1'

# Add argument parser at the top of the script
def parse_arguments():
    parser = argparse.ArgumentParser(description='Process conversations with OpenAI API')
    parser.add_argument('--num-rows', type=int, default=None,
                      help='Number of rows to process (default: all rows)')
    parser.add_argument('--input-file', type=str, default='input_data.xlsx',
                      help='Input Excel file path (default: input_data.xlsx)')
    parser.add_argument('--output-file', type=str, default='output_data_v2.xlsx',
                      help='Output Excel file path (default: output_data_v2.xlsx)')
    parser.add_argument('--sheet', type=str, default='Trang tính1',
                      help='Excel sheet name to process (default: Trang tính1)')
    parser.add_argument('--batch-size', type=int, default=4,
                      help='Number of items to process in each batch (default: 4)')
    parser.add_argument('--max-workers', type=int, default=4,
                      help='Maximum number of worker threads (default: 4)')
    return parser.parse_args()

def process_batch(batch_rows: List[Dict]):
    output_rows = []
    for row in batch_rows:
        order = row.get('order', 'default_order')  # Gán giá trị mặc định nếu không có cột 'order'
        prompt = row['system_prompt']
        # Kiểm tra xem cột 'conversation_history' có tồn tại không
        conversation_history = row.get('conversation_history', None)  # Gán None nếu không có cột 'conversation_history'
        inputs = [row['user_input']]
        
        logger.info(f"Processing order {order}")
        
        responses, response_times, chat_messages, model_config = process_conversation(
            order, prompt, inputs, conversation_history
        )
        
        # Copy all columns and add new data
        new_row = row.copy()
        new_row.update({
            'assistant_response': responses[0] if responses else None,
            'response_time': response_times[0] if response_times else None,
            'model_config': model_config
        })
        output_rows.append(new_row)
    
    return output_rows

def append_to_excel(filename, df):
    """Append DataFrame to existing Excel file without reading entire file."""
    try:
        with pd.ExcelWriter(filename, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            # Xác định vị trí bắt đầu append
            workbook = writer.book
            worksheet = workbook['Sheet1']  # hoặc sheet_name từ args
            start_row = worksheet.max_row
            
            # Append data mới
            df.to_excel(writer, 
                       index=False, 
                       header=False,
                       startrow=start_row)
            
        return True
    except Exception as e:
        logger.error(f"Error appending to Excel: {str(e)}")
        return False

def get_system_resources():
    """Lấy thông tin tài nguyên hệ thống."""
    try:
        cpu_count = multiprocessing.cpu_count()
        memory = psutil.virtual_memory()
        available_memory_gb = memory.available / (1024 * 1024 * 1024)  # Convert to GB
        cpu_percent = psutil.cpu_percent(interval=1)
        
        logger.info(f"System resources:")
        logger.info(f"- CPU cores: {cpu_count}")
        logger.info(f"- CPU usage: {cpu_percent}%")
        logger.info(f"- Available memory: {available_memory_gb:.2f}GB")
        logger.info(f"- Memory usage: {memory.percent}%")
        
        return {
            'cpu_count': cpu_count,
            'available_memory_gb': available_memory_gb,
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent
        }
    except Exception as e:
        logger.error(f"Error getting system resources: {str(e)}")
        return None

def optimize_batch_parameters(total_rows: int, args):
    """Tối ưu batch_size và max_workers dựa trên tài nguyên hệ thống."""
    resources = get_system_resources()
    if not resources:
        logger.warning("Using default parameters due to resource check failure")
        return args.batch_size, args.max_workers
    
    # Tối ưu max_workers
    recommended_workers = min(
        resources['cpu_count'],  # Không vượt quá số CPU cores
        int(8 * (100 - resources['cpu_percent']) / 100),  # Giảm nếu CPU đang cao
        int(resources['available_memory_gb'])  # Khoảng 1 worker/GB RAM available
    )
    max_workers = max(1, min(recommended_workers, args.max_workers))
    
    # Tối ưu batch_size
    memory_based_batch = int(resources['available_memory_gb'] * 1024)  # ~1MB per row estimate
    cpu_based_batch = int(20 * (100 - resources['cpu_percent']) / 100)  # Giảm batch size nếu CPU cao
    
    recommended_batch = min(
        memory_based_batch,
        cpu_based_batch,
        max(1, total_rows // (max_workers * 2))  # Ít nhất 2 batches per worker
    )
    batch_size = max(1, min(recommended_batch, args.batch_size))
    
    logger.info(f"Optimized parameters:")
    logger.info(f"- Original batch_size: {args.batch_size}, max_workers: {args.max_workers}")
    logger.info(f"- Recommended batch_size: {batch_size}, max_workers: {max_workers}")
    
    return batch_size, max_workers

def monitor_resources(stop_event, interval=30):
    """Monitor tài nguyên hệ thống trong quá trình xử lý."""
    while not stop_event.is_set():
        resources = get_system_resources()
        if resources:
            # Cảnh báo nếu tài nguyên gần cạn
            if resources['cpu_percent'] > 90:
                logger.warning("High CPU usage detected!")
            if resources['memory_percent'] > 90:
                logger.warning("High memory usage detected!")
        time.sleep(interval)

def main():
    args = parse_arguments()
    
    SCRIPTS_FOLDER = Path(__file__).parent
    INPUT_FILE = SCRIPTS_FOLDER / args.input_file
    OUTPUT_FILE = SCRIPTS_FOLDER / args.output_file

    df_input = pd.read_excel(INPUT_FILE, sheet_name=args.sheet)
    rows_to_process = df_input if args.num_rows is None else df_input.head(args.num_rows)
    
    # Tối ưu parameters
    batch_size, max_workers = optimize_batch_parameters(len(rows_to_process), args)
    
    all_rows = rows_to_process.to_dict('records')
    batches = [all_rows[i:i + batch_size] for i in range(0, len(all_rows), batch_size)]
    
    # Tạo file output với headers
    cols_order = list(df_input.columns) + ['assistant_response', 'response_time', 'model_config']
    pd.DataFrame(columns=cols_order).to_excel(OUTPUT_FILE, index=False)
    
    # Khởi động monitor thread
    stop_monitoring = threading.Event()
    monitor_thread = threading.Thread(target=monitor_resources, args=(stop_monitoring,))
    monitor_thread.start()
    
    try:
        processed_count = 0
        failed_batches = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_batch, batch) for batch in batches]
            
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                try:
                    batch_results = future.result()
                    batch_df = pd.DataFrame(batch_results)[cols_order]
                    
                    for attempt in range(3):
                        if append_to_excel(OUTPUT_FILE, batch_df):
                            processed_count += len(batch_results)
                            logger.info(f"Appended batch {i+1}. Total processed: {processed_count}")
                            break
                        else:
                            if attempt < 2:
                                logger.warning(f"Retry {attempt + 1} for batch {i+1}")
                                time.sleep(2)
                            else:
                                logger.error(f"Failed to append batch {i+1} after 3 attempts")
                                failed_batches.append((i, batch_results))
                                
                except Exception as e:
                    logger.error(f"Error processing batch {i+1}: {str(e)}")
                    failed_batches.append((i, None))

        # Xử lý lại các batch thất bại
        if failed_batches:
            logger.info(f"Retrying {len(failed_batches)} failed batches...")
            for batch_index, batch_results in failed_batches:
                if batch_results:
                    batch_df = pd.DataFrame(batch_results)[cols_order]
                    if append_to_excel(OUTPUT_FILE, batch_df):
                        processed_count += len(batch_results)
                        logger.info(f"Successfully retried batch {batch_index+1}")
                    else:
                        logger.error(f"Permanently failed to append batch {batch_index+1}")

    finally:
        # Dừng monitor thread
        stop_monitoring.set()
        monitor_thread.join()
        
        # Log kết quả cuối cùng
        logger.info(f"Processing completed. Total rows processed: {processed_count}")
        get_system_resources()  # Log tình trạng tài nguyên cuối cùng

if __name__ == "__main__":
    main()

