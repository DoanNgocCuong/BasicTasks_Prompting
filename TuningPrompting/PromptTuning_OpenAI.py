# 

# @title OPENAI
import json
import pandas as pd
import time
import openai
from openai import OpenAIError

from dotenv import load_dotenv
import os
load_dotenv()

# Replace 'your_api_key_here' with your actual OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# @title OPENAI KO CÓ MESSAGE HISTORY
def process_conversation(order, base_prompt, inputs):
    responses = []
    response_times = []
    # Initialize the message history with the system message (prompt)
    message_history = [{"role": "system", "content": base_prompt}]


    for user_input in inputs:
        # Add the current user input to the message history
        message_history.append({"role": "user", "content": user_input})

        start_time = time.time()
        try_count = 0
        while try_count < 3:
            try:
                completion = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=message_history,   
                    temperature=0,
                    max_tokens=6000,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                end_time = time.time()
                response_content = completion.choices[0].message.content
                # Add the assistant's response to the message history
                message_history.append({"role": "assistant", "content": response_content})

                responses.append(response_content)
                response_times.append(end_time - start_time)

                # Print the completion output here
                print(f"Order {order}, Input: '{user_input}', Response: '{response_content}', Time: {end_time - start_time:.2f}s\n====")
                break
            except OpenAIError:
                try_count += 1
                if try_count >= 3:
                    responses.append("Request failed after 2 retries.")
                    response_times.append("-")
                    print(f"Order {order}, Input: '{user_input}', Response: 'Request failed after 2 retries.', Time: -")
                else:
                    time.sleep(3)  # Wait for 10 seconds before retrying

    # Reset the message history for the next order
    return  responses, response_times, message_history

sheet_name = 'prompting'

# Load the input Excel file
df_input = pd.read_excel(r'D:\OneDrive - Hanoi University of Science and Technology\ITE10-DS&AI-HUST\Learn&Task\PRODUCT_THECOACH\Đã đẩy lên GITHUB\BasicTasks_Prompting\TuningPrompting\input_data.xlsx', sheet_name=sheet_name)

# Set the number of rows to process
num_rows_to_process = int(input("Enter the number of rows to process: "))

# List to store rows before appending them to the DataFrame
output_rows = []

for index, row in df_input.head(num_rows_to_process).iterrows():
    order = row['order']
    prompt = row['prompt']
    inputs = [row['user_input']]

    responses, response_times, message_history = process_conversation(order, prompt, inputs)

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