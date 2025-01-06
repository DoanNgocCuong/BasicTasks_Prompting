import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import argparse
from def_ApiClientB import AICoachAPI
from export_conversations_to_excel import export_conversations_to_excel
from def_simulate_with_openai import simulate_with_openai
from def_simulate_with_api import simulate_with_api

# Load environment variables
load_dotenv()

# Get the directory containing the script
SCRIPT_DIR = Path(__file__).parent

def init_new_conversation(use_api_for_roleB=False):
    """Khởi tạo mới hoàn toàn các clients và conversation cho mỗi dòng"""
    # Tạo mới OpenAI client
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Tạo mới API client nếu dùng API
    api_client = None
    if use_api_for_roleB:
        api_client = AICoachAPI()
        # Khởi tạo conversation mới
        if not api_client.init_conversation():
            print("[ERROR] Failed to initialize API conversation")
            return None, None
        
    return openai_client, api_client

def main(start_row=None, num_rows=None, input_file='2PromptingTuning.xlsx', output_file='result.xlsx', use_api_for_roleB=False):
    try:
        # Convert input and output paths to absolute paths
        input_path = SCRIPT_DIR / input_file
        output_path = SCRIPT_DIR / output_file

        print(f"\n=== Processing Settings ===")
        print(f"Input file: {input_path}")
        print(f"Output file: {output_path}")
        print(f"Using API for RoleB: {use_api_for_roleB}")

        # Check if input file exists
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Load data
        df = pd.read_excel(input_path)
        total_rows = len(df)
        
        # Calculate rows to process
        start_idx = start_row if start_row is not None else 0
        end_idx = min(start_idx + num_rows, total_rows) if num_rows else total_rows
        
        all_messages = []
        for index, row in df.iloc[start_idx:end_idx].iterrows():
            print(f"\n=== Processing Row {index + 1} ===")
            
            # Khởi tạo mới hoàn toàn cho mỗi dòng
            openai_client, api_client = init_new_conversation(use_api_for_roleB)
            if use_api_for_roleB and api_client is None:
                print(f"Skipping row {index + 1} due to API initialization failure")
                continue
            
            # Simulate conversation
            try:
                if use_api_for_roleB:
                    message_history, response_times = simulate_with_api(row, openai_client, api_client)
                else:
                    message_history, response_times = simulate_with_openai(row, openai_client)
                
                # Prepare export data
                initial_message_count = len(json.loads(row['initialConversationHistory'])) if not pd.isna(row['initialConversationHistory']) else 0

                for i, msg in enumerate(message_history):
                    response_time = 0
                    if i >= initial_message_count:  # Chỉ tính response time cho new messages
                        response_idx = i - initial_message_count
                        response_time = response_times[response_idx] if response_idx < len(response_times) else 0
                        
                    all_messages.append([
                        msg['role'],
                        msg['content'],
                        response_time,  # 0 cho initial messages, thời gian thực cho new messages
                        row['roleA_prompt'],
                        row['roleB_prompt'] if not use_api_for_roleB else "Using API"
                    ])
                all_messages.append(['Separator', '-------------------', 0, '', ''])
                
            except Exception as e:
                print(f"Error processing row {index + 1}: {str(e)}")
                continue
        
        # Export results
        export_conversations_to_excel(all_messages, output_path)
        
    except FileNotFoundError as e:
        print(f"File Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process conversations from Excel file')
    parser.add_argument('--start-row', type=int, help='Start row index (0-based)')
    parser.add_argument('--num-rows', type=int, help='Number of rows to process')
    parser.add_argument('--input', type=str, default='2PromptingTuning.xlsx',
                        help='Input Excel file name (should be in the same directory as the script)')
    parser.add_argument('--output', type=str, default='result.xlsx',
                        help='Output Excel file name')
    parser.add_argument('--use-api', action='store_true',
                        help='Use AICoachAPI for RoleB instead of OpenAI')
    
    args = parser.parse_args()
    main(args.start_row, args.num_rows, args.input, args.output, args.use_api) 