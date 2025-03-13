from openai import OpenAI
import time
import json
from utils_convert_roles_for_api import convert_roles_for_api

def generate_roleA_response(client, roleA_prompt, message_history):
    """Generate response for roleA"""
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
        temperature=0,
        max_completion_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    end_time = time.time()
    
    roleA_message = response.choices[0].message.content
    print(f"\nRoleA Response: {roleA_message}")
    print(f"Response Time: {end_time - start_time:.2f}s")
    
    return roleA_message, end_time - start_time 