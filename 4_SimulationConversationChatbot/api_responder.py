import requests
import uuid

HEADERS = {"Content-Type": "application/json"}

# Generate unique conversation_id
def generate_conversation_id():
    return str(uuid.uuid4())

# Initialize conversation
def init_conversation(bot_id, conversation_id, init_url):
    payload = {"bot_id": bot_id, "conversation_id": conversation_id, "input_slots": {}}
    response = requests.post(init_url, json=payload, headers=HEADERS)
    return response.json()

# Send user input to API
def send_message(conversation_id, message, webhook_url):
    payload = {"conversation_id": conversation_id, "message": message}
    response = requests.post(webhook_url, json=payload, headers=HEADERS)
    return response.json()
