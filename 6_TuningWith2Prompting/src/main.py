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

# Load environment variables
load_dotenv()

# Get the directory containing the script
SCRIPT_DIR = Path(__file__).parent

def init_new_conversation(use_api=False, bot_id=31):
    """Khởi tạo mới hoàn toàn các clients và conversation cho mỗi dòng"""
    # Tạo mới OpenAI client
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Tạo mới API client nếu dùng API
    api_client = None
    if use_api:
        api_client = AICoachAPI(bot_id=bot_id)
        # Khởi tạo conversation mới
        if not api_client.init_conversation():
            print("[ERROR] Failed to initialize API conversation")
            return None, None
        
    return openai_client, api_client

def main(start_row=None, num_rows=None, input_file='2PromptingTuning.xlsx', output_file='result.xlsx', bot_id=31):
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
            
        for index, row in df.iloc[start_idx:end_idx].iterrows():
            print(f"\n=== Processing Row {index + 1}/{end_idx} ===")
            
            use_api = str(row['useApiOrPrompt']).lower() == 'api'
            print(f"Using {'API' if use_api else 'Prompt'} for RoleB")
            
            # Initialize new conversation for each row
            openai_client, api_client = init_new_conversation(use_api, bot_id)
            if use_api and api_client is None:
                print(f"Skipping row {index + 1} due to API initialization failure")
                continue
            
            try:
                # Simulate conversation
                if use_api:
                    message_history, response_times, full_log = simulate_with_api(row, openai_client, api_client)
                else:
                    message_history, response_times = simulate_with_openai(row, openai_client)
                    # Initialize empty full_log for non-API case
                    full_log = [''] * len(message_history)
                
                # Check for exit condition in the last message if it's from roleB
                should_exit = False
                if message_history and message_history[-1]['role'] == 'assistant':
                    last_message = message_history[-1]['content']
                    should_exit = check_exit_condition(last_message)
                    if should_exit:
                        print("Exit condition detected in roleB's response. Ending conversation.")
                
                # Prepare current row data
                current_messages = []
                initial_message_count = 0
                if not use_api and not pd.isna(row['initialConversationHistory']):
                    initial_message_count = len(json.loads(row['initialConversationHistory']))

                for i, msg in enumerate(message_history):
                    response_time = 0
                    if i >= initial_message_count:
                        response_idx = i - initial_message_count
                        response_time = response_times[response_idx] if response_idx < len(response_times) else 0
                    
                    # Get full log for the current message
                    current_full_log = full_log[i] if use_api and i < len(full_log) else ''
                    
                    current_messages.append([
                        msg['role'],
                        msg['content'],
                        response_time,
                        row['roleA_prompt'],
                        row['roleB_prompt'] if not use_api else f"Using API (Bot ID: {bot_id})",
                        row['useApiOrPrompt'],
                        current_full_log  # Add full log data
                    ])
                
                # Add separator after the last message of the current row
                current_messages.append(['Separator', f'--- End of Row {index + 1} ---', 0, '', '', '', ''])
                
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
                print(f"Completed row {index + 1}/{end_idx}")
                
                # If exit condition was detected, break the loop
                if should_exit:
                    print(f"Stopping further processing due to exit condition in row {index + 1}")
                    break
                
            except Exception as e:
                print(f"Error processing row {index + 1}: {str(e)}")
                continue
        
        print("\n=== Processing Complete ===")
        
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
    parser.add_argument('--bot-id', type=int, default=31,
                        help='Bot ID for the API conversation')
    
    args = parser.parse_args()
    main(args.start_row, args.num_rows, args.input, args.output, args.bot_id) 
    ...