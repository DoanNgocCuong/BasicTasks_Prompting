from def_promptA import generate_roleA_response
from openai import OpenAI
import os

def generate_roleA_message(client, roleA_prompt, message_history):
    """Wrapper for roleA response generation"""
    return generate_roleA_response(client, roleA_prompt, message_history)

def create_roleA_client():
    """Create OpenAI client for roleA"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise Exception("OpenAI API key not found in environment variables")
    return OpenAI(api_key=api_key)