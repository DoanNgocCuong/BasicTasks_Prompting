import json
import pandas as pd
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_data(file_path):
    """Load conversation data from an Excel file."""
    return pd.read_excel(file_path)

def parse_conversation_history(history_str):
    """Parse conversation history from JSON string."""
    if pd.isna(history_str) or not history_str:
        return []
    try:
        history = json.loads(history_str)
        # Validate format
        for msg in history:
            if not isinstance(msg, dict) or 'role' not in msg or 'content' not in msg:
                print(f"Warning: Invalid message format in history: {msg}")
                return []
            # Validate role values
            if msg['role'] not in ['roleA', 'roleB']:
                print(f"Warning: Invalid role in message: {msg['role']}")
                return []
        return history
    except json.JSONDecodeError as e:
        print(f"Error parsing conversation history: {e}")
        return []

def simulate_conversation(row):
    """Simulate a conversation based on the row of data."""
    message_history = []
    response_times = []
    conversationTurnCount = 0

    # Extract settings from Excel row
    roleA_prompt = row['roleA_prompt']           # Prompt cho roleA
    roleB_prompt = row['roleB_prompt']           # Prompt cho roleB
    initialConversationHistory = row['initialConversationHistory']  # JSON string chứa lịch sử hội thoại ban đầu
    maxTurns = row['maxTurns']                   # Số lượt tối đa cho cuộc hội thoại

    # Parse and add conversation history if exists
    history = parse_conversation_history(initialConversationHistory)
    if history:
        message_history.extend(history)
        print("\n=== Initial Conversation History ===")
        for msg in history:
            print(f"{msg['role']}: {msg['content']}")
    
    # Start conversation loop
    while conversationTurnCount < maxTurns:
        try:
            # Generate roleA message
            start_time = time.time()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": roleA_prompt}] + 
                        [{"role": "user", "content": json.dumps(message_history)}],
                temperature=0.3
            )
            end_time = time.time()
            roleA_message = response.choices[0].message.content
            message_history.append({"role": "roleA", "content": roleA_message})
            response_times.append(end_time - start_time)
            print(f"\nRoleA: {roleA_message}")
            
            # Generate roleB response
            start_time = time.time()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": roleB_prompt}] + 
                        [{"role": "user", "content": json.dumps(message_history)}],
                temperature=0
            )
            end_time = time.time()
            roleB_message = response.choices[0].message.content
            message_history.append({"role": "roleB", "content": roleB_message})
            response_times.append(end_time - start_time)
            print(f"RoleB: {roleB_message}")
            
            conversationTurnCount += 1
            time.sleep(1)

        except Exception as e:
            print(f"Error during conversation: {str(e)}")
            break

    return message_history, response_times

def export_conversations_to_excel(all_messages, output_path):
    """Export all conversations and response times to an Excel file."""
    try:
        df_export = pd.DataFrame(all_messages, columns=['Role', 'Content', 'Response_Time'])
        df_export.to_excel(output_path, index=False)
        print(f"Conversations exported to {output_path}")
    except PermissionError:
        print("Error: Please close the Excel file before saving.")

def main():
    try:
        input_file = '6_TuningWith2Prompting/2PromptingTuning.xlsx'
        output_file = 'result.xlsx'
        df = load_data(input_file)
        
        all_messages = []
        
        for index, row in df.iterrows():
            print(f"\n=== Processing Conversation {index + 1} ===")
            message_history, response_times = simulate_conversation(row)
            
            # Add messages to export list
            for i, msg in enumerate(message_history):
                all_messages.append([
                    msg['role'],
                    msg['content'],
                    response_times[i] if i < len(response_times) else 0
                ])
            all_messages.append(['Separator', '-------------------', 0])
        
        export_conversations_to_excel(all_messages, output_file)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
