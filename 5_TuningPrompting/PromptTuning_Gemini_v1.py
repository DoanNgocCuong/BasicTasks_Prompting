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
import google.generativeai as genai
from typing import List, Dict, Any

load_dotenv()

# Remove OpenAI-specific imports and configurations
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Remove OpenAI initialization and only keep Gemini
print(f"Google API Key (last 5): ...{os.getenv('GOOGLE_API_KEY')[-5:]}")

# Update Gemini initialization with generation config
generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
gemini_model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config=generation_config
)

class ModelConfig:
    def __init__(self, provider: str, model_name: str, api_key: str, temperature: float = 0, max_tokens: int = 6000):
        self.provider = provider
        self.model_name = model_name
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    @property
    def full_model_name(self) -> str:
        return f"{self.provider}:{self.model_name}"

# @title OPENAI KO CÓ MESSAGE HISTORY
def process_conversation(order, base_prompt, inputs, conversation_history=None):
    all_responses = []
    all_response_times = []
    
    for model_config in model_configs:
        responses = []
        response_times = []
        
        # Start a new chat session
        chat_session = gemini_model.start_chat(history=[])
        
        # Add system prompt if exists
        if base_prompt:
            chat_session.send_message(base_prompt)
        
        # Handle conversation history
        if conversation_history and not pd.isna(conversation_history):
            try:
                history_messages = json.loads(conversation_history)
                if isinstance(history_messages, list):
                    for msg in history_messages:
                        if isinstance(msg, dict) and 'content' in msg:
                            chat_session.send_message(msg['content'])
            except json.JSONDecodeError as e:
                print(f"Error parsing conversation history: {e}")
        
        for user_input in inputs:
            start_time = time.time()
            try_count = 0
            while try_count < 3:
                try:
                    if not model_config.api_key:
                        raise ValueError("Missing Gemini API key")
                    
                    response = chat_session.send_message(user_input)
                    end_time = time.time()
                    response_content = response.text
                    responses.append(response_content)
                    response_times.append(end_time - start_time)
                    break
                    
                except Exception as e:
                    try_count += 1
                    print(f"DEBUG - {model_config.provider} API Error on attempt {try_count}: {str(e)}")
                    if try_count >= 3:
                        responses.append(f"Request failed after 2 retries: {str(e)}")
                        response_times.append(-1)
                    else:
                        time.sleep(3)
        
        all_responses.append(responses)
        all_response_times.append(response_times)
    
    return all_responses, all_response_times

# Update model configs to only include Gemini
model_configs = [
    ModelConfig("gemini", "gemini-1.5-flash", api_key=os.getenv('GOOGLE_API_KEY'))
]

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
    
    responses, response_times = process_conversation(
        order, prompt, inputs, conversation_history
    )

    for model_idx, model_config in enumerate(model_configs):
        for i, user_input in enumerate(inputs):
            output_rows.append({
                'order': order,
                'model': model_config.full_model_name,
                'prompt': prompt,
                'user_input': user_input,
                'assistant_response': responses[model_idx][i],
                'response_time': response_times[model_idx][i]
            })

# Create a DataFrame from the list of output rows
df_output = pd.DataFrame(output_rows, columns=['order', 'model', 'prompt', 'user_input', 'assistant_response', 'response_time'])
# Save the results to an Excel file
try:
    df_output.to_excel('output_data.xlsx', index=False)  # Added .xlsx extension
    print("Data has been successfully saved to 'output_data.xlsx'")
except PermissionError:
    print("File is open. Please close the file and try again.")
