import json
import pandas as pd
import os
from typing import List, Dict, Any

class ConversationProcessor:
    def __init__(self):
        pass
    
    def load_json_data(self, filepath: str) -> Dict[Any, Any]:
        """
        Load dữ liệu từ file JSON
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"❌ Lỗi khi đọc file {filepath}: {e}")
            return {}
    
    def extract_conversations(self, data: Dict[Any, Any]) -> List[Dict[str, Any]]:
        """
        Trích xuất từng cặp USER-BOT, handle cả 2 orders:
        1. BOT_RESPONSE_CONVERSATION → USER (BOT trước USER)
        2. USER → BOT_RESPONSE_CONVERSATION (USER trước BOT)
        """
        if 'data' not in data:
            print("❌ Không tìm thấy key 'data' trong JSON")
            return []

        conversations = []
        prev_assistant = None

        for i, item in enumerate(data['data']):
            character = item.get('character', '')
            content = item.get('content', '').strip()
            if not content:
                continue

            if character == 'BOT_RESPONSE_CONVERSATION':
                prev_assistant = content

            elif character == 'USER':
                if prev_assistant is not None:
                    # Tạo chỉ 1 cặp: assistant trước và user hiện tại
                    current_conversation = [
                        {"role": "assistant", "content": prev_assistant},
                        {"role": "user", "content": content}
                    ]

                    # Tìm câu FAST_RESPONSE tiếp theo (nếu có)
                    next_fast_response = ""
                    for j in range(i+1, len(data['data'])):
                        next_item = data['data'][j]
                        if next_item.get('character') == 'FAST_RESPONSE':
                            next_content = next_item.get('content', '').strip()
                            if next_content:
                                next_fast_response = next_content
                                break

                    # Tìm BOT_RESPONSE_CONVERSATION tiếp theo (nếu có)
                    next_bot_response = ""
                    for j in range(i+1, len(data['data'])):
                        next_item = data['data'][j]
                        if next_item.get('character') == 'BOT_RESPONSE_CONVERSATION':
                            next_content = next_item.get('content', '').strip()
                            if next_content:
                                next_bot_response = next_content
                                break

                    conversations.append({
                        'conversation': current_conversation,
                        'next_fast_response': next_fast_response,
                        'next_bot_response': next_bot_response
                    })
                else:
                    # Không có assistant phía trước, tìm BOT_RESPONSE_CONVERSATION sau USER này
                    next_assistant = None
                    for j in range(i+1, len(data['data'])):
                        next_item = data['data'][j]
                        if next_item.get('character') == 'BOT_RESPONSE_CONVERSATION':
                            next_content = next_item.get('content', '').strip()
                            if next_content:
                                next_assistant = next_content
                                break
                    
                    if next_assistant:
                        # Tạo conversation với BOT sau USER
                        current_conversation = [
                            {"role": "assistant", "content": next_assistant},
                            {"role": "user", "content": content}
                        ]

                        # Tìm câu FAST_RESPONSE tiếp theo (nếu có)
                        next_fast_response = ""
                        for j in range(i+1, len(data['data'])):
                            next_item = data['data'][j]
                            if next_item.get('character') == 'FAST_RESPONSE':
                                next_content = next_item.get('content', '').strip()
                                if next_content:
                                    next_fast_response = next_content
                                    break

                        # Tìm BOT_RESPONSE_CONVERSATION tiếp theo sau BOT hiện tại (nếu có)
                        next_bot_response = ""
                        bot_found = False
                        for j in range(i+1, len(data['data'])):
                            next_item = data['data'][j]
                            if next_item.get('character') == 'BOT_RESPONSE_CONVERSATION':
                                if not bot_found:
                                    bot_found = True  # Skip BOT đầu tiên (đã dùng làm assistant)
                                    continue
                                else:
                                    next_content = next_item.get('content', '').strip()
                                    if next_content:
                                        next_bot_response = next_content
                                        break

                        conversations.append({
                            'conversation': current_conversation,
                            'next_fast_response': next_fast_response,
                            'next_bot_response': next_bot_response
                        })
                    else:
                        # Thực sự không tìm thấy BOT nào, bỏ qua
                        continue

        return conversations

    def format_conversation_column(self, conversation: List[Dict[str, str]]) -> str:
        """
        Format conversation thành string JSON
        """
        return json.dumps(conversation, ensure_ascii=False)
    
    def process_to_dataframe(self, conversations: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Chuyển đổi conversations thành DataFrame
        """
        processed_data = []
        
        for conv in conversations:
            processed_data.append({
                'BOT_RESPONSE_CONVERSATION_with_USER': self.format_conversation_column(conv['conversation']),
                'FAST_RESPONSE_next': conv['next_fast_response'],
                'BOT_RESPONSE_CONVERSATION_next': conv['next_bot_response'], 
                'response_time': ''  # ← THÊM DÒNG NÀY
            })
        
        return pd.DataFrame(processed_data)
    
    def process_file(self, input_filepath: str, output_filepath: str) -> bool:
        """
        Xử lý file JSON và xuất ra Excel
        """
        try:
            # Load dữ liệu
            data = self.load_json_data(input_filepath)
            if not data:
                return False
            
            # Trích xuất conversations
            conversations = self.extract_conversations(data)
            if not conversations:
                print("❌ Không tìm thấy conversation nào")
                return False
            
            # Tạo DataFrame
            df = self.process_to_dataframe(conversations)
            
            # Xuất ra Excel
            df.to_excel(output_filepath, index=False, engine='openpyxl')
            print(f"✅ Đã xuất dữ liệu ra: {output_filepath}")
            print(f"📊 Số lượng conversations: {len(conversations)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi xử lý file: {e}")
            return False

def process_all_input_files():
    """
    Xử lý tất cả file trong folder input
    """
    processor = ConversationProcessor()
    
    if not os.path.exists('input'):
        print("❌ Folder 'input' không tồn tại")
        return
    
    # Tạo folder output nếu chưa có
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Xử lý từng file JSON trong folder input
    for filename in os.listdir('input'):
        if filename.endswith('.json'):
            input_path = os.path.join('input', filename)
            output_filename = filename.replace('.json', '_processed.xlsx')
            output_path = os.path.join('output', output_filename)
            
            print(f"\n🔄 Đang xử lý: {filename}")
            processor.process_file(input_path, output_path)

if __name__ == "__main__":
    process_all_input_files()
