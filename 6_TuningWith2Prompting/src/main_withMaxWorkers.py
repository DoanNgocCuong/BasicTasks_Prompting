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
from def_promptB import check_exit_condition  # Import the exit condition check
import concurrent.futures
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get the directory containing the script
SCRIPT_DIR = Path(__file__).parent

def init_new_conversation(use_api=False, bot_id=31):
    """Initialize new clients and conversation for each row"""
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    api_client = None
    if use_api:
        api_client = AICoachAPI(bot_id=bot_id)
        if not api_client.init_conversation():
            print("[ERROR] Failed to initialize API conversation")
            return None, None
        
    return openai_client, api_client

def process_row(row, bot_id):
    """Process a single row of conversation"""
    use_api = str(row['useApiOrPrompt']).lower() == 'api'
    openai_client, api_client = init_new_conversation(use_api, bot_id)
    
    if use_api and api_client is None:
        return None, None, True  # Indicate failure to initialize API
    
    try:
        if use_api:
            message_history, response_times, full_log = simulate_with_api(row, openai_client, api_client)
        else:
            message_history, response_times = simulate_with_openai(row, openai_client)
            full_log = [''] * len(message_history)  # Initialize empty full_log for non-API case
        
        # Check for exit condition in the last message if it's from roleB
        should_exit = False
        if message_history and message_history[-1]['role'] == 'assistant':
            last_message = message_history[-1]['content']
            should_exit = check_exit_condition(last_message)
            if should_exit:
                print("Exit condition detected in roleB's response. Ending conversation.")
        
        return message_history, response_times, should_exit
    
    except Exception as e:
        print(f"Error processing row: {str(e)}")
        return None, None, False  # Indicate processing error

def main(start_row=None, num_rows=None, input_file='2PromptingTuning.xlsx', output_file='result.xlsx', bot_id=31, max_workers=4):
    try:
        input_path = SCRIPT_DIR / input_file
        output_path = SCRIPT_DIR / output_file

        print(f"\n=== Processing Settings ===")
        print(f"Input file: {input_path}")
        print(f"Output file: {output_path}")
        print(f"Bot ID: {bot_id}")

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Load data
        df = pd.read_excel(input_path)
        total_rows = len(df)
        
        # Calculate rows to process
        start_idx = start_row if start_row is not None else 0
        end_idx = min(start_idx + num_rows, total_rows) if num_rows else total_rows
        
        print(f"Processing rows {start_idx + 1} to {end_idx}")
        
        # Prepare to process rows in parallel
        rows_to_process = df.iloc[start_idx:end_idx].to_dict('records')
        should_exit = False
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_row, row, bot_id): row for row in rows_to_process}
            for future in concurrent.futures.as_completed(futures):
                row = futures[future]
                try:
                    message_history, response_times, exit_condition = future.result()
                    if exit_condition:
                        should_exit = True
                        break
                    
                    # Prepare current row data for export
                    current_messages = []
                    for i, msg in enumerate(message_history):
                        response_time = response_times[i] if i < len(response_times) else 0
                        current_messages.append([
                            msg['role'],
                            msg['content'],
                            response_time,
                            row['roleA_prompt'],
                            row['roleB_prompt'] if not use_api else f"Using API (Bot ID: {bot_id})",
                            row['useApiOrPrompt'],
                            ''  # Placeholder for full log
                        ])
                    
                    # Add separator after the last message of the current row
                    current_messages.append(['Separator', f'--- End of Row {row["order"]} ---', 0, '', '', '', ''])
                    
                    # Export immediately after processing each row
                    df_new = pd.DataFrame(current_messages, columns=[
                        'Role', 
                        'Content', 
                        'Response Time',
                        'RoleA Prompt',
                        'RoleB Prompt',
                        'useApiOrPrompt',
                        'Full Log'
                    ])
                    export_conversations_to_excel(df_new, output_path)
                    print(f"Completed row {row['order']}")
                    
                except Exception as e:
                    print(f"Error processing row: {str(e)}")
        
        if should_exit:
            print("Stopping further processing due to exit condition.")
        
        print("\n=== Processing Complete ===")
        
    except FileNotFoundError as e:
        print(f"File Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process conversations from Excel file with max workers')
    parser.add_argument('--start-row', type=int, help='Start row index (0-based)')
    parser.add_argument('--num-rows', type=int, help='Number of rows to process')
    parser.add_argument('--input', type=str, default='2PromptingTuning.xlsx',
                        help='Input Excel file name (should be in the same directory as the script)')
    parser.add_argument('--output', type=str, default='result.xlsx',
                        help='Output Excel file name')
    parser.add_argument('--bot-id', type=int, default=31,
                        help='Bot ID for the API conversation')
    parser.add_argument('--max-workers', type=int, default=4,
                        help='Maximum number of worker threads')
    
    args = parser.parse_args()
    main(args.start_row, args.num_rows, args.input, args.output, args.bot_id, args.max_workers) 
    ...