import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import argparse
from def_promptA_v2 import generate_roleA_response
from def_promptB_v2 import generate_roleB_response, create_client
from export_conversations_to_excel import export_conversations_to_excel

# Load environment variables
load_dotenv()

# Get the directory containing the script
SCRIPT_DIR = Path(__file__).parent

def simulate_conversation(row, openai_client, api_client, use_api_for_roleB=False):
    """
    Simulate a conversation based on the row of data
    Args:
        row: DataFrame row containing conversation settings
        openai_client: OpenAI client for roleA
        api_client: AICoachAPI client for roleB
        use_api_for_roleB: If True, use AICoachAPI for roleB, else use OpenAI
    """
    message_history = []
    response_times = []
    conversationTurnCount = 0

    # Extract and validate settings
    roleA_prompt = str(row['roleA_prompt']) if not pd.isna(row['roleA_prompt']) else ""
    roleB_prompt = str(row['roleB_prompt']) if not pd.isna(row['roleB_prompt']) else ""
    initialConversationHistory = row['initialConversationHistory']
    maxTurns = int(row['maxTurns']) if not pd.isna(row['maxTurns']) else 3

    print("\n=== Initial Settings ===")
    print(f"RoleA Prompt: {roleA_prompt[:100]}..." if roleA_prompt else "RoleA Prompt: None")
    print(f"RoleB Prompt: {roleB_prompt[:100]}..." if roleB_prompt else "RoleB Prompt: None")
    print(f"Max Turns: {maxTurns}")
    print(f"Using API for RoleB: {use_api_for_roleB}")

    # Process conversation history
    if not pd.isna(initialConversationHistory):
        try:
            history = json.loads(initialConversationHistory)
            message_history.extend(history)
            print("\nInitial conversation history loaded")
        except json.JSONDecodeError as e:
            print(f"Error parsing conversation history: {e}")

    # Conversation loop
    while conversationTurnCount < maxTurns:
        try:
            # RoleA's turn
            roleA_message, roleA_time = generate_roleA_response(openai_client, roleA_prompt, message_history)
            message_history.append({"role": "roleA", "content": roleA_message})
            response_times.append(roleA_time)

            # RoleB's turn
            client = api_client if use_api_for_roleB else openai_client
            roleB_message, roleB_time = generate_roleB_response(
                client, 
                roleB_prompt, 
                message_history,
                use_api=use_api_for_roleB
            )
            message_history.append({"role": "roleB", "content": roleB_message})
            response_times.append(roleB_time)

            conversationTurnCount += 1

        except Exception as e:
            print(f"Error during conversation: {str(e)}")
            break

    return message_history, response_times

def main(num_rows=None, input_file='2PromptingTuning.xlsx', output_file='result.xlsx', use_api_for_roleB=False):
    """
    Main function to process conversations
    Args:
        num_rows: Số dòng cần xử lý (None để xử lý tất cả)
        input_file: Tên file Excel input
        output_file: Tên file Excel output
        use_api_for_roleB: Nếu True, sử dụng AICoachAPI cho roleB
    """
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

        # Create clients
        openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        api_client = create_client(use_api=True) if use_api_for_roleB else None

        # Load and process data
        df = pd.read_excel(input_path)
        total_rows = len(df)
        rows_to_process = min(num_rows or total_rows, total_rows)
        print(f"Total rows in file: {total_rows}")
        print(f"Rows to process: {rows_to_process}")
        
        all_messages = []
        for index, row in df.head(rows_to_process).iterrows():
            print(f"\n=== Processing Row {index + 1}/{rows_to_process} ===")
            
            message_history, response_times = simulate_conversation(
                row, 
                openai_client, 
                api_client, 
                use_api_for_roleB
            )
            
            # Prepare export data
            for i, msg in enumerate(message_history):
                all_messages.append([
                    msg['role'],
                    msg['content'],
                    response_times[i] if i < len(response_times) else 0,
                    row['roleA_prompt'],
                    row['roleB_prompt']
                ])
            all_messages.append(['Separator', '-------------------', 0, '', ''])
        
        # Export results
        export_conversations_to_excel(all_messages, output_path)
        
    except FileNotFoundError as e:
        print(f"File Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process conversations from Excel file')
    parser.add_argument('--rows', type=int, help='Number of rows to process (default: all rows)')
    parser.add_argument('--input', type=str, default='2PromptingTuning.xlsx',
                        help='Input Excel file name (should be in the same directory as the script)')
    parser.add_argument('--output', type=str, default='result.xlsx',
                        help='Output Excel file name')
    parser.add_argument('--use-api', action='store_true',
                        help='Use AICoachAPI for RoleB instead of OpenAI')
    
    args = parser.parse_args()
    main(args.rows, args.input, args.output, args.use_api) 