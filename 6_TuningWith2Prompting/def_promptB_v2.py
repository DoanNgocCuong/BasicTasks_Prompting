import time
import json
import requests
from openai import OpenAI
import os
from utils_convert_roles_for_api import convert_roles_for_api

class AICoachAPI:
    def __init__(self, base_url="http://103.253.20.13:9400"):
        """Khởi tạo với base URL của API"""
        self.base_url = base_url
        self.init_endpoint = f"{base_url}/personalized-ai-coach/api/v1/bot/initConversation"
        self.webhook_endpoint = f"{base_url}/personalized-ai-coach/api/v1/bot/webhook"
        self.current_conversation_id = None

    def init_conversation(self, bot_id=3):
        """Khởi tạo cuộc hội thoại mới"""
        conversation_id = f"conv_{int(time.time())}"
        payload = {
            "bot_id": bot_id,
            "conversation_id": conversation_id,
            "input_slots": {}
        }
        
        try:
            print(f"\n[AICoachAPI] Initializing conversation...")
            print(f"[AICoachAPI] Endpoint: {self.init_endpoint}")
            print(f"[AICoachAPI] Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                self.init_endpoint,
                headers={'Content-Type': 'application/json'},
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            print(f"[AICoachAPI] Init successful. Response: {json.dumps(response.json(), indent=2)}")
            self.current_conversation_id = conversation_id
            return True
            
        except requests.Timeout:
            print("[AICoachAPI] Error: Request timed out during initialization")
            return False
        except requests.RequestException as e:
            print(f"[AICoachAPI] Error during initialization: {str(e)}")
            return False

    def send_message(self, message):
        """Gửi tin nhắn tới bot"""
        if not self.current_conversation_id:
            print("[AICoachAPI] Error: No active conversation. Initializing new one...")
            if not self.init_conversation():
                return None

        payload = {
            "conversation_id": self.current_conversation_id,
            "message": message
        }
        
        try:
            print(f"\n[AICoachAPI] Sending message...")
            print(f"[AICoachAPI] Endpoint: {self.webhook_endpoint}")
            print(f"[AICoachAPI] Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                self.webhook_endpoint,
                headers={'Content-Type': 'application/json'},
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            response_data = response.json()
            print(f"[AICoachAPI] Message sent successfully. Response: {json.dumps(response_data, indent=2)}")
            return response_data.get('message', '')
            
        except requests.Timeout:
            print("[AICoachAPI] Error: Request timed out while sending message")
            return None
        except requests.RequestException as e:
            print(f"[AICoachAPI] Error sending message: {str(e)}")
            return None

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

def create_client(use_api=False):
    """Create appropriate client based on use_api flag"""
    if use_api:
        client = AICoachAPI()
        if not client.init_conversation():
            raise Exception("Failed to initialize AI Coach API")
        return client
    else:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise Exception("OpenAI API key not found in environment variables")
        return OpenAI(api_key=api_key) 