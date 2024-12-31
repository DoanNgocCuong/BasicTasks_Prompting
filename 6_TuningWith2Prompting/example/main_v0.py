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

def convert_roles_for_api(messages, is_roleA_turn=True):
    """
    Chuyển đổi roleA/roleB thành user/assistant cho OpenAI API
    is_roleA_turn: True nếu đang là lượt của roleA, False nếu là lượt của roleB
    """
    converted_messages = []
    for msg in messages:
        if is_roleA_turn:
            # Khi là lượt của roleA
            if msg["role"] == "roleA":
                role = "assistant"  # roleA's own messages become assistant
            else:
                role = "user"       # roleB's messages become user
        else:
            # Khi là lượt của roleB
            if msg["role"] == "roleB":
                role = "assistant"  # roleB's own messages become assistant
            else:
                role = "user"       # roleA's messages become user
        
        converted_messages.append({
            "role": role,
            "content": msg["content"]
        })
    return converted_messages

def simulate_conversation(row):
    """Simulate a conversation based on the row of data."""
    message_history = []
    response_times = []
    conversationTurnCount = 0

    # Extract settings from Excel row
    roleA_prompt = str(row['roleA_prompt']) if not pd.isna(row['roleA_prompt']) else ""
    roleB_prompt = str(row['roleB_prompt']) if not pd.isna(row['roleB_prompt']) else ""
    initialConversationHistory = row['initialConversationHistory']
    
    # Handle NaN in maxTurns with default value
    maxTurns = row['maxTurns']
    if pd.isna(maxTurns):
        maxTurns = 3  # Default value if NaN
    else:
        maxTurns = int(maxTurns)
    
    print("\n=== Initial Settings ===")
    print(f"RoleA Prompt: {roleA_prompt[:100]}..." if roleA_prompt else "RoleA Prompt: None")
    print(f"RoleB Prompt: {roleB_prompt[:100]}..." if roleB_prompt else "RoleB Prompt: None")
    print(f"Max Turns: {maxTurns}")

    # Parse and add conversation history if exists
    if pd.isna(initialConversationHistory):
        print("\nNo initial conversation history")
    else:
        history = parse_conversation_history(initialConversationHistory)
        if history:
            message_history.extend(history)
            print("\n=== Initial Conversation History ===")
            print(json.dumps(message_history, indent=2, ensure_ascii=False))
    
    # Start conversation loop
    while conversationTurnCount < maxTurns:
        try:
            # Generate roleA message
            print("\n=== RoleA Turn ===")
            print("Original message history:")
            print(json.dumps(message_history, indent=2, ensure_ascii=False))
            
            api_messages = [{"role": "system", "content": roleA_prompt}]
            if message_history:
                converted_history = convert_roles_for_api(message_history, is_roleA_turn=True)
                api_messages.extend(converted_history)
                print("\nConverted history for RoleA:")
                print(json.dumps(api_messages, indent=2, ensure_ascii=False))
            
            start_time = time.time()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages,
                temperature=0
            )
            end_time = time.time()
            roleA_message = response.choices[0].message.content
            message_history.append({"role": "roleA", "content": roleA_message})
            response_times.append(end_time - start_time)
            print(f"\nRoleA Response: {roleA_message}")
            print(f"Response Time: {end_time - start_time:.2f}s")
            
            # Generate roleB response
            print("\n=== RoleB Turn ===")
            print("Original message history:")
            print(json.dumps(message_history, indent=2, ensure_ascii=False))
            
            api_messages = [{"role": "system", "content": roleB_prompt}]
            if message_history:
                converted_history = convert_roles_for_api(message_history, is_roleA_turn=False)
                api_messages.extend(converted_history)
                print("\nConverted history for RoleB:")
                print(json.dumps(api_messages, indent=2, ensure_ascii=False))
            
            start_time = time.time()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages,
                temperature=0
            )
            end_time = time.time()
            roleB_message = response.choices[0].message.content
            message_history.append({"role": "roleB", "content": roleB_message})
            response_times.append(end_time - start_time)
            print(f"\nRoleB Response: {roleB_message}")
            print(f"Response Time: {end_time - start_time:.2f}s")
            
            conversationTurnCount += 1
            print(f"\n=== End of Turn {conversationTurnCount}/{maxTurns} ===")
            time.sleep(1)

        except Exception as e:
            print(f"\nError during conversation: {str(e)}")
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
