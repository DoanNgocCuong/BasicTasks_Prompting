import concurrent.futures
import pandas as pd
from def_ApiClientB import AICoachAPI
from def_simulate_with_openai import simulate_with_openai
from def_simulate_with_api import simulate_with_api
from export_conversations_to_excel import export_conversations_to_excel
from def_promptB import check_exit_condition

def process_row(row, bot_id):
    """Process a single row of conversation"""
    use_api = str(row['useApiOrPrompt']).lower() == 'api'
    openai_client, api_client = init_new_conversation(use_api, bot_id)
    
    if use_api and api_client is None:
        return None, None, True, use_api  # Indicate failure to initialize API and return use_api
    
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
        
        return message_history, response_times, should_exit, use_api  # Return use_api
    
    except Exception as e:
        print(f"Error processing row: {str(e)}")
        return None, None, False, use_api  # Indicate processing error and return use_api

def process_batches(rows_to_process, bot_id, max_workers, output_path):
    """Process rows in batches using multiple workers."""
    should_exit = False
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_row, row, bot_id): row for row in rows_to_process}
        for future in concurrent.futures.as_completed(futures):
            row = futures[future]
            try:
                message_history, response_times, exit_condition, use_api = future.result()
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
                print(f"Error processing batch: {str(e)}")
    
    return should_exit 