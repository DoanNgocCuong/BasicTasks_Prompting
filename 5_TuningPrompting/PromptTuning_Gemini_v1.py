import json
import pandas as pd
import time
import os
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore', category=ResourceWarning)

def init_gemini():
    """Initialize Gemini model and config"""
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("Missing Google API Key. Please check your .env file")
    print(f"Google API Key (last 5): ...{api_key[-5:]}")

    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    ), generation_config

def process_conversation(model, order, base_prompt, inputs, conversation_history=None):
    """Process a single conversation"""
    print(f"\n=== Processing Conversation ===")
    print(f"Order: {order}")
    print(f"Base Prompt: {base_prompt[:100]}...")
    
    responses = []
    response_times = []
    
    chat = model.start_chat(history=[])
    
    try:
        # Add system prompt if exists
        if base_prompt and not pd.isna(base_prompt):
            chat.send_message(base_prompt)
        
        # Handle conversation history
        if conversation_history and not pd.isna(conversation_history):
            try:
                history_messages = json.loads(conversation_history)
                if isinstance(history_messages, list):
                    for msg in history_messages:
                        if isinstance(msg, dict) and 'content' in msg:
                            chat.send_message(msg['content'])
            except json.JSONDecodeError as e:
                print(f"Error parsing conversation history: {e}")
        
        # Process new inputs
        for user_input in inputs:
            if pd.isna(user_input):
                responses.append("Request failed: Empty input")
                response_times.append(-1)
                continue
                
            start_time = time.time()
            try_count = 0
            while try_count < 3:
                try:
                    print(f"\nAttempt {try_count + 1}/3 to call Gemini API")
                    response = chat.send_message(user_input)
                    end_time = time.time()
                    
                    response_content = response.text.strip()
                    responses.append(response_content)
                    response_times.append(end_time - start_time)
                    
                    print(f"Order {order}, Input: '{user_input}', Response: '{response_content}', Time: {end_time - start_time:.2f}s\n====")
                    break
                    
                except Exception as e:
                    try_count += 1
                    print(f"DEBUG - API Error on attempt {try_count}: {str(e)}")
                    if try_count >= 3:
                        responses.append("Request failed after 2 retries.")
                        response_times.append(-1)
                    else:
                        print("Waiting 3 seconds before retry...")
                        time.sleep(3)
    finally:
        del chat
    
    return responses, response_times

def save_results(df_output, filename='output_gemini_v2.xlsx'):
    """Save results to Excel file"""
    try:
        df_output.to_excel(filename, index=False)
        print(f"Data has been successfully saved to '{filename}'")
    except PermissionError:
        print("File is open. Please close the file and try again.")

def main():
    """Main execution function"""
    sheet_name = 'TestingPromptOnDataset'
    SCRIPTS_FOLDER = Path(__file__).parent
    df_input = pd.read_excel(SCRIPTS_FOLDER / 'input_data.xlsx', sheet_name=sheet_name)
    df_input['order'] = df_input['order'].fillna(method='ffill')

    print("\nAvailable columns in DataFrame:")
    print(df_input.columns.tolist())

    num_rows_to_process = int(input("Enter the number of rows to process: "))
    output_rows = []
    
    model, generation_config = init_gemini()
    
    try:
        for index, row in df_input.head(num_rows_to_process).iterrows():
            print(f"\n=== Processing Row {index} ===")
            print(f"Row data:")
            print(f"- Order: {row['order']}")
            print(f"- Prompt: {row['system_prompt'][:100]}...")
            print(f"- User Input: {row['user_input']}")
            
            responses, response_times = process_conversation(
                model,
                row['order'],
                row['system_prompt'],
                [row['user_input']],
                row['conversation_history']
            )

            output_row = row.copy()
            output_row['model'] = json.dumps({
                "provider": "gemini",
                "model": "gemini-1.5-flash",
                "temperature": generation_config["temperature"],
                "top_p": generation_config["top_p"],
                "top_k": generation_config["top_k"],
                "max_tokens": generation_config["max_output_tokens"],
                "stream": False
            }, indent=2)
            output_row['assistant_response'] = responses[0]
            output_row['response_time'] = response_times[0]
            output_rows.append(output_row)
    finally:
        del model

    df_output = pd.DataFrame(output_rows)
    save_results(df_output)

if __name__ == "__main__":
    main()