import time
import json
from openai import OpenAI
from utils_convert_roles_for_api import convert_roles_for_api

def check_exit_condition(text):
    """Check if the text contains exit phrases like "Bye" or "Hẹn gặp lại"
    Returns True if exit condition is met, False otherwise"""
    exit_phrases = ["bye", "hẹn gặp lại", "tạm biệt", "goodbye"]
    
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    for phrase in exit_phrases:
        if phrase in text_lower:
            print(f"Exit condition detected: '{phrase}' found in response")
            return True
    
    return False

def generate_roleB_response(client, roleB_prompt, message_history):
    """Generate response for roleB"""
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
        model="gpt-4o-2024-11-20",
        messages=api_messages,
        temperature=0.3,
        max_completion_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    end_time = time.time()
    
    roleB_message = response.choices[0].message.content
    print(f"\nRoleB Response: {roleB_message}")
    print(f"Response Time: {end_time - start_time:.2f}s")
    
    return roleB_message, end_time - start_time
