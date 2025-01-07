import json
import pandas as pd
import time
from def_promptA import generate_roleA_response

def simulate_with_api(row, openai_client, api_client):
    """Simulate conversation using OpenAI for RoleA and API for RoleB"""
    message_history = []
    response_times = []
    conversationTurnCount = 0

    # Extract settings
    roleA_prompt = str(row['roleA_prompt']) if not pd.isna(row['roleA_prompt']) else ""
    maxTurns = int(row['maxTurns']) if not pd.isna(row['maxTurns']) else 3

    print("\n=== Initial Settings ===")
    print(f"RoleA Prompt: {roleA_prompt[:100]}..." if roleA_prompt else "RoleA Prompt: None")
    print(f"Max Turns: {maxTurns}")

    # Get initial message from history
    initial_message = "sẵn sàng"  # default
    if not pd.isna(row['initialConversationHistory']):
        try:
            history = json.loads(row['initialConversationHistory'])
            if history and history[0]["role"] == "roleA":
                initial_message = history[0]["content"]
                # Add initial roleA message to history
                message_history.append({"role": "roleA", "content": initial_message})
                response_times.append(0)  # 0 for initial message
            print(f"\nUsing initial message: {initial_message}")
        except json.JSONDecodeError as e:
            print(f"Error parsing conversation history: {e}")

    # Start with RoleB using the initial message
    api_response = api_client.send_message(initial_message)
    
    if api_response and "text" in api_response:
        roleB_message = api_response["text"][0]
        message_history.append({"role": "roleB", "content": roleB_message})
        # Lấy process_time từ API response và làm tròn 6 chữ số
        process_time = round(float(api_response.get("process_time", 0)), 6)
        response_times.append(process_time)
    else:
        print("[ERROR] Failed to get initial response from API")
        return message_history, response_times

    # Start conversation loop
    while conversationTurnCount < maxTurns:
        try:
            # RoleA turn with OpenAI
            roleA_message, roleA_time = generate_roleA_response(
                openai_client,
                roleA_prompt,
                message_history
            )
            message_history.append({"role": "roleA", "content": roleA_message})
            # Làm tròn response time của OpenAI
            response_times.append(round(roleA_time, 6))

            # RoleB turn with API
            api_response = api_client.send_message(roleA_message)

            if api_response and "text" in api_response:
                roleB_message = api_response["text"][0]
                message_history.append({"role": "roleB", "content": roleB_message})
                # Lấy process_time từ API response và làm tròn 6 chữ số
                process_time = round(float(api_response.get("process_time", 0)), 6)
                response_times.append(process_time)
            else:
                print("[ERROR] Failed to get response from API")
                break

            conversationTurnCount += 1
            print(f"\n=== End of Turn {conversationTurnCount}/{maxTurns} ===")
            time.sleep(1)

        except Exception as e:
            print(f"\nError during conversation: {str(e)}")
            break

    return message_history, response_times
