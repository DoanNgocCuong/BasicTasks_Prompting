import time
import json
import requests
from openai import OpenAI
import os
from utils_convert_roles_for_api import convert_roles_for_api


def generate_roleB_response(client, roleB_prompt, message_history, use_api=False):
    """Generate response for roleB"""
    print("\n=== RoleB Turn ===")
    
    # Ensure message_history is a list
    if isinstance(message_history, str):
        print("Warning: message_history is a string, converting to list...")
        message_history = [{"role": "roleA", "content": message_history}]
    
    print("Original message history:")
    print(json.dumps(message_history, indent=2, ensure_ascii=False))
    
    start_time = time.time()
    
    try:
        if use_api:
            # Using AI Coach API
            last_message = message_history[-1]['content'] if message_history else "sẵn sàng"
            response_data = client.send_message(last_message)
            
            if response_data is None:
                raise Exception("Failed to get response from AI Coach API")
            
            # Extract text from response
            if isinstance(response_data, dict) and 'text' in response_data:
                roleB_message = response_data['text'][0] if response_data['text'] else ""
            else:
                roleB_message = response_data
                
        else:
            # Using OpenAI
            api_messages = [{"role": "system", "content": roleB_prompt}]
            if message_history:
                converted_history = convert_roles_for_api(message_history, is_roleA_turn=False)
                api_messages.extend(converted_history)
                print("\nConverted history for RoleB:")
                print(json.dumps(api_messages, indent=2, ensure_ascii=False))
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=api_messages,
                temperature=0,
                max_completion_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            roleB_message = response.choices[0].message.content
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"\nRoleB Response: {roleB_message}")
        print(f"Response Time: {response_time:.2f}s")
        
        return roleB_message, response_time
        
    except Exception as e:
        print(f"\nError in generate_roleB_response: {str(e)}")
        return None, 0
