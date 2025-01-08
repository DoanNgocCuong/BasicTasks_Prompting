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
import aisuite as ai
from typing import List, Dict, Any

# Get the current file's directory
SCRIPTS_FOLDER = Path(__file__).parent

# Load .env file from the correct path
env_path = SCRIPTS_FOLDER / '.env'

print(f"\nLoading .env from: {env_path.absolute()}")
load_dotenv(env_path, override=True)

# Print API keys with more details for debugging
openai_key = os.getenv('OPENAI_API_KEY')
groq_key = os.getenv('GROQ_API_KEY')

print("\n=== API Keys Verification ===")
print(f"OpenAI API Key found: {'Yes' if openai_key else 'No'}")
print(f"OpenAI API Key (last 5): ...{openai_key[-5:] if openai_key else 'NOT FOUND'}")
print(f"Groq API Key found: {'Yes' if groq_key else 'No'}")
print(f"Groq API Key (last 5): ...{groq_key[-5:] if groq_key else 'NOT FOUND'}")
print(f"Groq API Key length: {len(groq_key) if groq_key else 0}")
print("===========================\n")

# Verify keys are present
if not openai_key or not groq_key:
    raise ValueError("Missing API keys. Please check your .env file")


# Initialize OpenAI client
client = ai.Client()

class ModelConfig:
    def __init__(self, provider: str, model_name: str, api_key: str, 
                 temperature: float = 0, 
                 max_tokens: int = 6000,
                 top_p: float = 1,
                 frequency_penalty: float = 0.0,
                 presence_penalty: float = 0.0):
        self.provider = provider
        self.model_name = model_name
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        
    @property
    def full_model_name(self) -> str:
        return f"{self.provider}:{self.model_name}"

# Initialize model configs with both models
model_configs = [
    ModelConfig("openai", "gpt-4o-mini", api_key=os.getenv('OPENAI_API_KEY')),
    # ModelConfig("groq", "llama-3.3-70b-versatile", api_key=os.getenv('GROQ_API_KEY')),
]

def process_conversation(order, base_prompt, inputs, conversation_history=None):
    all_responses = []
    all_response_times = []
    
    for model_config in model_configs:
        responses = []
        response_times = []
        chat_messages = []
        
        # System message
        chat_messages.append({"role": "system", "content": base_prompt})
        
        # History handling
        if conversation_history and not pd.isna(conversation_history):
            try:
                history_messages = json.loads(conversation_history)
                if isinstance(history_messages, list):
                    for msg in history_messages:
                        if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                            chat_messages.append(msg)
            except json.JSONDecodeError as e:
                print(f"Error parsing conversation history: {e}")
        
        for user_input in inputs:
            chat_messages.append({"role": "user", "content": user_input})
            
            # Add detailed logging before API call
            print("\n=== Before API Call ===")
            print(f"Model: {model_config.full_model_name}")
            print(f"Temperature: {model_config.temperature}")
            print(f"Max tokens: {model_config.max_tokens}")
            print("\nChat Messages:")
            for msg in chat_messages:
                print(f"[{msg['role']}]: {msg['content'][:100]}...")
            print("\nAttempting API call...")
            
            start_time = time.time()
            try_count = 0
            while try_count < 3:
                try:
                    print(f"\nAttempt {try_count + 1}/3 to call {model_config.full_model_name} API")
                    completion = client.chat.completions.create(
                        model=model_config.full_model_name,
                        messages=chat_messages,
                        temperature=model_config.temperature,
                        max_tokens=model_config.max_tokens,
                        top_p=model_config.top_p,
                        frequency_penalty=model_config.frequency_penalty,
                        presence_penalty=model_config.presence_penalty
                    )
                    end_time = time.time()
                    response_content = completion.choices[0].message.content
                    responses.append(response_content)
                    response_times.append(end_time - start_time)
                    
                    chat_messages.append({"role": "assistant", "content": response_content})
                    break
                    
                except Exception as e:
                    try_count += 1
                    print(f"DEBUG - {model_config.full_model_name} API Error on attempt {try_count}: {str(e)}")
                    if try_count >= 3:
                        responses.append(f"Request failed after 2 retries: {str(e)}")
                        response_times.append(-1)
                    else:
                        time.sleep(3)
        
        all_responses.append(responses)
        all_response_times.append(response_times)
    
    return all_responses, all_response_times

sheet_name = 'TestingPromptOnDataset'

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
    
    # Lấy dữ liệu từ row, không lọc NaN
    order = row['order']
    prompt = row['system_prompt']
    conversation_history = row['conversation_history']
    user_input = row['user_input']
    
    print(f"Input data validation:")
    print(f"- Order: {order}")
    print(f"- Prompt: {prompt}")
    print(f"- History: {conversation_history}")
    print(f"- User input: {user_input}")
    
    # Nếu user_input là NaN, set responses và times là error message
    if pd.isna(user_input):
        print(f"Row {index} has NaN user_input")
        for model_idx, model_config in enumerate(model_configs):
            model_info = {
                "provider": model_config.provider,
                "model": model_config.model_name,
                "max_tokens": model_config.max_tokens,
                "temperature": model_config.temperature,
                "top_p": model_config.top_p,
                "frequency_penalty": model_config.frequency_penalty,
                "presence_penalty": model_config.presence_penalty,
                "stream": False
            }
            
            output_row = row.copy()
            output_row['model'] = json.dumps(model_info, indent=2)
            output_row['assistant_response'] = "Request failed after 2 retries."
            output_row['response_time'] = -1
            output_rows.append(output_row)
        continue
    
    inputs = [user_input]
    responses, response_times = process_conversation(
        order, prompt, inputs, conversation_history
    )

    for model_idx, model_config in enumerate(model_configs):
        for i, user_input in enumerate(inputs):
            model_info = {
                "provider": model_config.provider,
                "model": model_config.model_name,
                "max_tokens": model_config.max_tokens,
                "temperature": model_config.temperature,
                "top_p": model_config.top_p,
                "frequency_penalty": model_config.frequency_penalty,
                "presence_penalty": model_config.presence_penalty,
                "stream": False
            }
            
            # Copy tất cả các cột từ file gốc
            output_row = row.copy()  # Copy toàn bộ dữ liệu từ row gốc
            # Thêm các cột mới
            output_row['model'] = json.dumps(model_info, indent=2)
            output_row['assistant_response'] = responses[model_idx][i]
            output_row['response_time'] = response_times[model_idx][i]
            
            output_rows.append(output_row)

# Create DataFrame với đúng thứ tự cột
df_output = pd.DataFrame(output_rows)
# Save the results to an Excel file
try:
    df_output.to_excel('output_data_v3.xlsx', index=False)  # Added .xlsx extension
    print("Data has been successfully saved to 'output_data.xlsx'")
except PermissionError:
    print("File is open. Please close the file and try again.")
