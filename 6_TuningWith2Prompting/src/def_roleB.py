from def_promptB import generate_roleB_response
from def_ApiClientB import AICoachAPI
from openai import OpenAI
import os

def generate_roleB_message(client, roleB_prompt, message_history, use_api=False):
    """Wrapper for roleB response generation"""
    return generate_roleB_response(client, roleB_prompt, message_history, use_api)

def create_roleB_client(use_api=False):
    """Create appropriate client for roleB"""
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