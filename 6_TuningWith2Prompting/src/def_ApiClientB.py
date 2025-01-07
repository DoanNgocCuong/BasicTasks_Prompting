import time
import json
import requests
from openai import OpenAI
import os
from utils_convert_roles_for_api import convert_roles_for_api


class AICoachAPI:
    def __init__(self, base_url="http://103.253.20.13:9400", timeout=30):
        """Khởi tạo với base URL của API"""
        self.base_url = base_url
        self.init_endpoint = f"{base_url}/personalized-ai-coach/api/v1/bot/initConversation"
        self.webhook_endpoint = f"{base_url}/personalized-ai-coach/api/v1/bot/webhook"
        self.current_conversation_id = None
        self.timeout = timeout

    def init_conversation(self, bot_id=29):
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
                timeout=self.timeout
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
                timeout=self.timeout
            )
            response.raise_for_status()
            
            response_data = response.json()
            print(f"[AICoachAPI] Message sent successfully. Response: {json.dumps(response_data, indent=2)}")
            return response_data
            
        except requests.Timeout:
            print("[AICoachAPI] Error: Request timed out while sending message")
            return None
        except requests.RequestException as e:
            print(f"[AICoachAPI] Error sending message: {str(e)}")
            return None
