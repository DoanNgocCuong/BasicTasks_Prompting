import pandas as pd
import requests
import json
import time
import argparse
import re

def init_conversation(bot_id, conversation_id):
    url = "http://103.253.20.13:9400/personalized-ai-coach/api/v1/bot/initConversation"
    payload = {
        "bot_id": bot_id,
        "conversation_id": conversation_id,
        "input_slots": {}
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def send_message(conversation_id, message, history):
    url = "http://103.253.20.13:9400/personalized-ai-coach/api/v1/bot/webhook"
    payload = {
        "conversation_id": conversation_id,
        "message": message,
        "history": history,
        "question_idx": 1
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def clean_json_string(json_str):
    if pd.isna(json_str):
        return None
        
    # Remove any BOM characters and extra whitespace
    cleaned = json_str.replace('\ufeff', '').strip()
    
    try:
        # First try to parse as-is
        json.loads(cleaned)
        return cleaned
    except json.JSONDecodeError:
        # If fails, try to fix quotes in content
        try:
            # Find all content values and escape quotes within them
            pattern = r'"content":\s*"(.*?)"(?=\s*[,}])'
            
            def escape_quotes(match):
                content = match.group(1)
                # Escape any unescaped quotes within content
                fixed_content = content.replace('"', '\\"')
                return f'"content": "{fixed_content}"'
            
            cleaned = re.sub(pattern, escape_quotes, cleaned)
            
            # Validate JSON after cleaning
            json.loads(cleaned)
            print(f"Successfully fixed JSON by escaping quotes")
            return cleaned
            
        except Exception as e:
            print(f"Failed to fix JSON: {str(e)}")
            print(f"Original string: {json_str}")
            print(f"Cleaned string: {cleaned}")
            raise e

def process_conversation(input_file, output_file, bot_id):
    # Read input Excel file
    df = pd.read_excel(input_file)
    print(f"Loaded input file: {input_file} with {len(df)} rows")
    print(f"Using bot_id: {bot_id}")
    
    # Create a copy of input dataframe
    output_df = df.copy()
    
    # Add new columns
    output_df['full_log'] = ''
    output_df['text_response'] = ''
    output_df['process_time'] = ''
    
    # Process each row
    for index, row in df.iterrows():
        print(f"\nProcessing row {index + 1}/{len(df)}")
        try:
            # Clean and parse conversation history
            try:
                cleaned_json = clean_json_string(row['conversation_history'])
                if cleaned_json is None:
                    raise ValueError("Empty conversation history")
                    
                history = json.loads(cleaned_json)
                print(f"Successfully parsed JSON for row {index + 1}")
                
            except json.JSONDecodeError as je:
                print(f"JSON Error at row {index + 1}. Showing raw conversation_history:")
                print(row['conversation_history'])
                print(f"Error details: {str(je)}")
                raise je
            
            # Generate unique conversation_id for each row
            conversation_id = f"123456_{index}"
            
            # Initialize new conversation for each row
            try:
                init_response = init_conversation(bot_id, conversation_id)
                print(f"Successfully initialized conversation {conversation_id} for row {index + 1}")
            except Exception as e:
                error = f"Init conversation failed: {str(e)}"
                print(error)
                output_df.at[index, 'full_log'] = json.dumps({"error": error}, ensure_ascii=False)
                output_df.at[index, 'text_response'] = f"ERROR: {error}"
                output_df.at[index, 'process_time'] = '-1'
                continue
            
            # Validate history structure
            if not isinstance(history, list):
                error = "History must be a list format"
                output_df.at[index, 'full_log'] = json.dumps({"error": error}, ensure_ascii=False)
                output_df.at[index, 'text_response'] = f"ERROR: {error}"
                output_df.at[index, 'process_time'] = '-1'
                continue
                
            for msg in history:
                if not isinstance(msg, dict) or 'role' not in msg or 'content' not in msg:
                    error = "Invalid message format in history"
                    output_df.at[index, 'full_log'] = json.dumps({"error": error}, ensure_ascii=False)
                    output_df.at[index, 'text_response'] = f"ERROR: {error}"
                    output_df.at[index, 'process_time'] = '-1'
                    continue
            
            print(f"User message: {row['user_answer']}")
            
            # Convert roleA/roleB to user/assistant
            for msg in history:
                msg['role'] = 'user' if msg['role'] == 'roleA' else 'assistant'
            
            # Send message and get response
            try:
                response = send_message(conversation_id, row['user_answer'], history)
                process_time = response.get('process_time', 0)
                
                print(f"Response received (process time: {process_time:.3f}s): {response['text'][0] if response.get('text') else 'No text response'}")
                
                # Update output dataframe instead of df
                output_df.at[index, 'full_log'] = json.dumps(response, ensure_ascii=False)
                output_df.at[index, 'text_response'] = response['text'][0] if response.get('text') else ''
                output_df.at[index, 'process_time'] = f"{process_time:.3f}"
                
            except Exception as e:
                error = f"API call failed: {str(e)}"
                print(f"API Error at row {index + 1}: {error}")
                output_df.at[index, 'full_log'] = json.dumps({"error": error}, ensure_ascii=False)
                output_df.at[index, 'text_response'] = f"ERROR: {error}"
                output_df.at[index, 'process_time'] = '-1'
            
        except Exception as e:
            error = f"Unexpected error: {str(e)}"
            print(f"ERROR at row {index + 1}: {error}")
            output_df.at[index, 'full_log'] = json.dumps({"error": error}, ensure_ascii=False)
            output_df.at[index, 'text_response'] = f"ERROR: {error}"
            output_df.at[index, 'process_time'] = '-1'
        
        # Add small delay to avoid overwhelming the API
        time.sleep(0.5)
    
    # Save to new Excel file with all columns
    try:
        output_df.to_excel(output_file, index=False)
        print(f"\nSuccessfully saved output to: {output_file}")
        print(f"Output columns: {', '.join(output_df.columns)}")
    except Exception as e:
        print(f"Error saving output file: {str(e)}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process conversations with specified bot ID')
    parser.add_argument('--bot_id', type=int, required=True, help='Bot ID for the conversation')
    parser.add_argument('--input', type=str, default='input.xlsx', help='Input Excel file path')
    parser.add_argument('--output', type=str, default='output.xlsx', help='Output Excel file path')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run process_conversation with provided arguments
    process_conversation(args.input, args.output, args.bot_id)

if __name__ == "__main__":
    main()