# 

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
print(openai.api_key)
# @title OPENAI KO CÓ MESSAGE HISTORY
def process_conversation(order, base_prompt, inputs, conversation_history=None):
    print(f"\n=== Processing Conversation ===")
    print(f"Order: {order}")
    print(f"Base Prompt: {base_prompt[:100]}...")
    
    responses = []
    response_times = []
    chat_messages = []
    
    # 1. System message
    chat_messages.append({"role": "system", "content": base_prompt})
    print("\nSau khi thêm system message:")
    print(chat_messages)
    
    # 2. History - đơn giản hóa
    if conversation_history and not pd.isna(conversation_history):
        chat_messages.extend([
            {"role": "assistant", "content": "Chúng ta sẽ bắt đầu với cụm \"Thức dậy\". Hãy cùng mình nói cụm \"Thức dậy\" bằng tiếng anh nha"}
        ])
        print("\nSau khi thêm history:")
        print(chat_messages)
    
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
                    model="gpt-4o-mini",
                    messages=chat_messages,   
                    temperature=0,
                    max_tokens=6000,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                end_time = time.time()
                response_content = completion.choices[0].message.content
                # Add the assistant's response to the message history
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
    return  responses, response_times, chat_messages

sheet_name = 'TestingPromptOnDataset'

# Define the base paths
SCRIPTS_FOLDER = Path(__file__).parent

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
    
    responses, response_times, chat_messages = process_conversation(
        order, prompt, inputs, conversation_history
    )

    for i, user_input in enumerate(inputs):
        output_rows.append({
            'order': order,
            'prompt': prompt,  # Added column for original prompt
            'user_input': user_input,
            'assistant_response': responses[i],
            'response_time': response_times[i],

        })

# Create a DataFrame from the list of output rows
df_output = pd.DataFrame(output_rows, columns=['order', 'prompt', 'user_input', 'assistant_response', 'response_time'])
# Save the results to an Excel file
try:
    df_output.to_excel('output_data.xlsx', index=False)  # Added .xlsx extension
    print("Data has been successfully saved to 'output_data.xlsx'")
except PermissionError:
    print("File is open. Please close the file and try again.")
# ... existing code ...