import time
import json
from openai import OpenAI
from utils_convert_roles_for_api import convert_roles_for_api

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
        model="gpt-4o",
        messages=api_messages,
        temperature=0,
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
