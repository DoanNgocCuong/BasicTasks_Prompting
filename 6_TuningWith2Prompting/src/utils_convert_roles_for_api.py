def convert_roles_for_api(messages, is_roleA_turn=True):
    """
    Chuyển đổi roleA/roleB thành user/assistant cho OpenAI API
    is_roleA_turn: True nếu đang là lượt của roleA, False nếu là lượt của roleB
    """
    converted_messages = []
    for msg in messages:
        if is_roleA_turn:
            if msg["role"] == "roleA":
                role = "assistant"
            else:
                role = "user"
        else:
            if msg["role"] == "roleB":
                role = "assistant"
            else:
                role = "user"
        
        converted_messages.append({
            "role": role,
            "content": msg["content"]
        })
    return converted_messages 