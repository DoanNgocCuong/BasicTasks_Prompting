import json
import pandas as pd
import time
from def_promptA import generate_roleA_response
from def_promptB import generate_roleB_response

def simulate_with_openai(row, openai_client):
    """Simulate conversation using OpenAI for both roles"""
    message_history = []
    response_times = []
    conversationTurnCount = 0

    # Extract settings
    roleA_prompt = str(row['roleA_prompt']) if not pd.isna(row['roleA_prompt']) else ""
    roleB_prompt = str(row['roleB_prompt']) if not pd.isna(row['roleB_prompt']) else ""
    initialConversationHistory = row['initialConversationHistory']
    maxTurns = int(row['maxTurns']) if not pd.isna(row['maxTurns']) else 3

    print("\n=== Initial Settings ===")
    print(f"RoleA Prompt: {roleA_prompt[:100]}..." if roleA_prompt else "RoleA Prompt: None")
    print(f"RoleB Prompt: {roleB_prompt[:100]}..." if roleB_prompt else "RoleB Prompt: None")
    print(f"Max Turns: {maxTurns}")

    # Load initial history
    if not pd.isna(initialConversationHistory):
        try:
            history = json.loads(initialConversationHistory)
            message_history.extend(history)
            print("\n=== Initial Conversation History ===")
            print(json.dumps(message_history, indent=2, ensure_ascii=False))
        except json.JSONDecodeError as e:
            print(f"Error parsing conversation history: {e}")

    # Determine which role goes first based on last message in history
    start_with_roleB = False
    if message_history:
        last_message = message_history[-1]
        if last_message["role"] == "roleA":
            start_with_roleB = True
    
    # Start conversation loop
    while conversationTurnCount < maxTurns:
        try:
            if not start_with_roleB:
                # RoleA turn first
                roleA_message, roleA_time = generate_roleA_response(
                    openai_client,
                    roleA_prompt,
                    message_history
                )
                message_history.append({"role": "roleA", "content": roleA_message})
                response_times.append(roleA_time)

                # Then RoleB turn
                roleB_message, roleB_time = generate_roleB_response(
                    openai_client,
                    roleB_prompt,
                    message_history
                )
                message_history.append({"role": "roleB", "content": roleB_message})
                response_times.append(roleB_time)
            else:
                # RoleB turn first
                roleB_message, roleB_time = generate_roleB_response(
                    openai_client,
                    roleB_prompt,
                    message_history
                )
                message_history.append({"role": "roleB", "content": roleB_message})
                response_times.append(roleB_time)

                # Then RoleA turn
                roleA_message, roleA_time = generate_roleA_response(
                    openai_client,
                    roleA_prompt,
                    message_history
                )
                message_history.append({"role": "roleA", "content": roleA_message})
                response_times.append(roleA_time)

            conversationTurnCount += 1
            print(f"\n=== End of Turn {conversationTurnCount}/{maxTurns} ===")
            time.sleep(1)

        except Exception as e:
            print(f"\nError during OpenAI conversation: {str(e)}")
            break

    return message_history, response_times