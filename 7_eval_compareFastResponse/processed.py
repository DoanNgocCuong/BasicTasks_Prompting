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
        Trích xuất và tổ chức dữ liệu conversation
        """
        if 'data' not in data:
            print("❌ Không tìm thấy key 'data' trong JSON")
            return []
        
        conversations = []
        current_conversation = []
        
        for item in data['data']:
            character = item.get('character', '')
            content = item.get('content', '').strip()
            
            # Bỏ qua nếu content rỗng
            if not content:
                continue
                
            if character == 'BOT_RESPONSE_CONVERSATION':
                current_conversation.append({"role": "assistant", "content": content})
                
            elif character == 'USER':
                current_conversation.append({"role": "user", "content": content})
                
                # Khi gặp USER, tạo một conversation entry
                conversations.append({
                    'conversation': current_conversation.copy(),
                    'next_fast_response': '',
                    'next_bot_response': ''
                })
        
        # Cập nhật next_fast_response và next_bot_response
        for i, item in enumerate(data['data']):
            if item.get('character') == 'FAST_RESPONSE':
                # Tìm conversation tương ứng để cập nhật
                for conv in conversations:
                    if not conv['next_fast_response']:  # Cập nhật cho conversation chưa có fast_response
                        conv['next_fast_response'] = item.get('content', '')
                        break
            elif item.get('character') == 'BOT_RESPONSE_CONVERSATION' and item.get('content', '').strip():
                # Tìm conversation tương ứng để cập nhật next_bot_response
                for conv in conversations:
                    if not conv['next_bot_response']:  # Cập nhật cho conversation chưa có bot_response
                        conv['next_bot_response'] = item.get('content', '')
                        break
        
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
                'BOT_RESPONSE_CONVERSATION_next': conv['next_bot_response']
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
