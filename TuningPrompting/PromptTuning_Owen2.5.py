# @title 
import json
import pandas as pd
import time
import requests

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
                payload = {
                    "messages": message_history
                }
                response = requests.post(
                    'https://mentor-dev.fpt.ai/math-centerpiece-model',
                    headers={'Content-Type': 'application/json'},
                    json=payload
                )
                response.raise_for_status()
                end_time = time.time()
                result = response.json()
                print("Raw response:", json.dumps(result, indent=2))  # Print raw response
                response_content = result.get('response', {}).get('response', '')
                formatted_result = response_content.replace("\\n", "\n").replace("\\(", "$").replace("\\)", "$").replace("\\[", "$$").replace("\\]", "$$")
                print("Formatted result:", formatted_result)  # Print formatted result

                # Add the assistant's response to the message history
                message_history.append({"role": "assistant", "content": formatted_result})

                responses.append(formatted_result)
                response_times.append(end_time - start_time)

                # Print the completion output here
                print(f"Order {order}, Input: '{user_input}', Response: '{formatted_result}', Time: {end_time - start_time:.2f}s\n====")
                break
            except requests.RequestException as e:
                try_count += 1
                if try_count >= 3:
                    error_message = f"Error: {e.response.status_code} - {e.response.text}" if hasattr(e, 'response') else str(e)
                    responses.append(f"Request failed after 2 retries. {error_message}")
                    response_times.append("-")
                    print(f"Order {order}, Input: '{user_input}', Response: 'Request failed after 2 retries. {error_message}', Time: -")
                else:
                    time.sleep(3)  # Wait for 3 seconds before retrying

    # Reset the message history for the next order
    return responses, response_times, message_history

sheet_name = 'prompting'

# Load the input Excel file
df_input = pd.read_excel(r'input_data.xlsx', sheet_name=sheet_name)

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