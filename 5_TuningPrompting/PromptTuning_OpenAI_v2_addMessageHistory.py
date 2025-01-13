# @title OPENAI
import json
import pandas as pd
import time
import openai
from openai import OpenAIError
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

# Replace 'your_api_key_here' with your actual OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
print(openai.api_key[:10])
# @title OPENAI KO CÓ MESSAGE HISTORY
def process_conversation(order, base_prompt, inputs, conversation_history=None):
    print(f"\n=== Processing Conversation ===")
    print(f"Order: {order}")
    print(f"Base Prompt: {base_prompt[:100]}...")
    
    # Tạo model config dưới dạng JSON
    model_config = {
        "model": "gpt-4o-mini",
        "temperature": 0,
        "max_tokens": 6000,
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

sheet_name = 'dang2'

# Define the base paths
SCRIPTS_FOLDER = Path(__file__).parent
OUTPUT_FILE = SCRIPTS_FOLDER / 'output_data_v2.xlsx'

# Load the input Excel file
df_input = pd.read_excel(SCRIPTS_FOLDER / 'input_data.xlsx', sheet_name=sheet_name)

# Set the number of rows to process
num_rows_to_process = int(input("Enter the number of rows to process: "))

# List to store rows before appending them to the DataFrame
output_rows = []

print("\nAvailable columns in DataFrame:")
print(df_input.columns.tolist())

for index, row in df_input.head(num_rows_to_process).iterrows():
    print(f"\n=== Processing Row {index} ===")
    order = row['order']
    prompt = row['system_prompt']
    conversation_history = row['conversation_history']
    inputs = [row['user_input']]
    
    print(f"Row data:")
    print(f"- Order: {order}")
    print(f"- Prompt: {prompt[:100]}...")
    print(f"- User Input: {inputs[0]}")
    
    responses, response_times, chat_messages, model_config = process_conversation(
        order, prompt, inputs, conversation_history
    )

    # Copy all columns from input DataFrame
    new_row = row.to_dict()
    
    # Add new columns
    new_row.update({
        'assistant_response': responses[0] if responses else None,
        'response_time': response_times[0] if response_times else None,
        'model_config': model_config
    })
    
    output_rows.append(new_row)

# Create DataFrame with all original columns plus new ones
df_output = pd.DataFrame(output_rows)

# Reorder columns if needed
cols_order = list(df_input.columns) + ['assistant_response', 'response_time', 'model_config']
df_output = df_output[cols_order]

# Save to Excel using pathlib
try:
    df_output.to_excel(OUTPUT_FILE, index=False)
    print(f"Data has been successfully saved to '{OUTPUT_FILE}'")
except PermissionError:
    print(f"File '{OUTPUT_FILE}' is open. Please close the file and try again.")
