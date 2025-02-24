import pandas as pd
import json

# Đọc file Excel
def read_excel_file(file_path):
    df = pd.read_excel(file_path)
    df = df[['Role', 'Content', 'Full Log']]
    return df

# Tạo file Excel mới với định dạng yêu cầu
def create_new_excel_file(df, output_file_path):
    """
    Converts a conversation DataFrame into a structured Excel file with specific formatting requirements.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame containing conversation data with columns:
        - 'Role': Indicates the speaker (roleA for user, roleB for assistant, Separator for conversation breaks)
        - 'Content': The actual message content
        - 'Full Log': JSON string containing additional metadata like intents

    output_file_path : str
        Path where the processed Excel file will be saved

    Output DataFrame Columns:
    -----------------------
    - conversation_history: List of all messages up to current point in JSON format
    - previous_assistant_response: Last assistant message before current user message
    - user_answer: Current user message
    - next_assistant_response: Assistant's reply to current user message
    - full_log: Raw JSON metadata for the conversation
    - process_time: Time taken to process the conversation from full_log
    - INTENT_PREDICT_LLM: Predicted intent extracted from full_log
    - CUR_INTENT: Current intent extracted from full_log

    Notes:
    ------
    - Only processes rows where Role is 'roleA' (user messages)
    - Handles conversation separation using 'Separator' roles
    - Maintains conversation context through a running history
    - Automatically balances all column lengths in final output
    - JSON parsing is handled with error protection
    
    Example:
    --------
    >>> df = read_excel_file('input.xlsx')
    >>> create_new_excel_file(df, 'output.xlsx')
    # Creates a new Excel file with restructured conversation data
    """
    output_data = {
        "conversation_history": [],
        "previous_assistant_response": [],
        "user_answer": [],
        "next_assistant_response": [],
        "full_log": [],
        "process_time": [],
        "INTENT_PREDICT_LLM": [],
        "CUR_INTENT": []
    }
    
    conversation_history = []

    for index, row in df.iterrows():
        if row['Role'] == 'roleA':
            user_content = row["Content"]
            output_data["user_answer"].append(user_content)

            # Cập nhật previous_assistant_response
            if index > 0 and df.iloc[index - 1]['Role'] == 'roleB':
                previous_assistant_response = df.iloc[index - 1]["Content"]
            else:
                previous_assistant_response = ""
            output_data["previous_assistant_response"].append(previous_assistant_response)

            # Cập nhật next_assistant_response, full_log và các intent
            if index + 1 < len(df) and df.iloc[index + 1]['Role'] == 'roleB':
                next_assistant_response = df.iloc[index + 1]["Content"]
                full_log = df.iloc[index + 1]["Full Log"] if not pd.isna(df.iloc[index + 1]["Full Log"]) else ""
                
                # Lấy intent và process_time từ full_log
                try:
                    if full_log:
                        full_log_json = json.loads(full_log)
                        record = full_log_json.get('logs', {}).get('record', {})
                        intent_predict = record.get('INTENT_PREDICT_LLM', '')
                        cur_intent = record.get('CUR_INTENT', '')
                        # Lấy process_time từ root level
                        process_time = full_log_json.get('process_time', '')
                    else:
                        intent_predict = ''
                        cur_intent = ''
                        process_time = ''
                except (json.JSONDecodeError, AttributeError, KeyError):
                    intent_predict = ''
                    cur_intent = ''
                    process_time = ''
            else:
                next_assistant_response = ""
                full_log = ""
                intent_predict = ""
                cur_intent = ""
                process_time = ""
                
            output_data["next_assistant_response"].append(next_assistant_response)
            output_data["full_log"].append(full_log)
            output_data["process_time"].append(process_time)
            output_data["INTENT_PREDICT_LLM"].append(intent_predict)
            output_data["CUR_INTENT"].append(cur_intent)

            # Cập nhật conversation_history
            output_data["conversation_history"].append(
                '[\n    ' + ',\n    '.join(conversation_history) + ',\n    ' + f'{{"role": "roleB", "content": "{df.iloc[index + 1]["Content"]}"}}\n]'
            )
            
            conversation_history.append(f'{{"role": "{row["Role"]}", "content": "{user_content}"}}')

        elif row['Role'] == 'roleB':
            conversation_history.append(f'{{"role": "{row["Role"]}", "content": "{row["Content"]}"}}')

        elif row['Role'] == 'Separator':
            output_data["conversation_history"].append('--- End of Conversation ---')
            output_data["previous_assistant_response"].append("")
            output_data["user_answer"].append("")
            output_data["next_assistant_response"].append("")
            output_data["full_log"].append("")
            output_data["process_time"].append("")
            output_data["INTENT_PREDICT_LLM"].append("")
            output_data["CUR_INTENT"].append("")
            conversation_history = []
            continue

        if row['Role'] == 'roleA':
            output_data["conversation_history"][-1] = f'[\n    ' + ',\n    '.join(conversation_history[:-1]) + '\n]'

    # Kiểm tra và cân bằng độ dài các danh sách
    max_length = max(len(value) for value in output_data.values())
    for key in output_data:
        while len(output_data[key]) < max_length:
            output_data[key].append("")

    output_df = pd.DataFrame(output_data)
    output_df.to_excel(output_file_path, index=False)

# Đường dẫn đến file Excel cũ và file mới
input_file_path = './id33.xlsx'
output_file_path = './id33_processed.xlsx'


# Đọc dữ liệu từ file cũ
df = read_excel_file(input_file_path)

# Tạo file Excel mới
create_new_excel_file(df, output_file_path)