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
        Trích xuất conversation với 3 turns history (sliding window).
        Mỗi conversation chứa tối đa 3 cặp USER-BOT gần nhất (6 messages).
        Handle cả 2 orders: BOT→USER và USER→BOT
        """
        if 'data' not in data:
            print("❌ Không tìm thấy key 'data' trong JSON")
            return []

        conversations = []
        current_conversation = []
        MAX_TURNS = 3  # Tối đa 3 turns (6 messages)
        
        # Collect all valid messages first
        messages = []
        for item in data['data']:
            character = item.get('character', '')
            content = item.get('content', '').strip()
            if content and character in ['BOT_RESPONSE_CONVERSATION', 'USER']:
                messages.append({
                    'character': character,
                    'content': content,
                    'original_index': len(messages)
                })
        
        # Build conversation progressively
        for i, msg in enumerate(messages):
            if msg['character'] == 'BOT_RESPONSE_CONVERSATION':
                current_conversation.append({"role": "assistant", "content": msg['content']})
            elif msg['character'] == 'USER':
                current_conversation.append({"role": "user", "content": msg['content']})
                
                # Apply sliding window - keep only last 3 turns (6 messages)
                if len(current_conversation) > MAX_TURNS * 2:
                    current_conversation = current_conversation[-(MAX_TURNS * 2):]
                
                # Ensure conversation starts with assistant (reorder if needed)
                formatted_conversation = self._ensure_assistant_first(current_conversation.copy())
                
                if formatted_conversation:
                    # Find next responses after current USER
                    next_fast_response = ""
                    next_bot_response = ""
                    
                    # Look for responses in original data after current position
                    original_data = data['data']
                    user_found = False
                    
                    for j, item in enumerate(original_data):
                        if item.get('content', '').strip() == msg['content'] and item.get('character') == 'USER':
                            if not user_found:
                                user_found = True
                                # Find FAST_RESPONSE after this USER
                                for k in range(j+1, len(original_data)):
                                    next_item = original_data[k]
                                    if next_item.get('character') == 'FAST_RESPONSE':
                                        next_content = next_item.get('content', '').strip()
                                        if next_content:
                                            next_fast_response = next_content
                                            break
                                
                                # Find next BOT_RESPONSE_CONVERSATION
                                for k in range(j+1, len(original_data)):
                                    next_item = original_data[k]
                                    if next_item.get('character') == 'BOT_RESPONSE_CONVERSATION':
                                        next_content = next_item.get('content', '').strip()
                                        if next_content:
                                            next_bot_response = next_content
                                            break
                                break
                    
                    conversations.append({
                        'conversation': formatted_conversation,
                        'next_fast_response': next_fast_response,
                        'next_bot_response': next_bot_response,
                        'context_length': len(formatted_conversation)  # Debug info
                    })
        
        return conversations
    
    def _ensure_assistant_first(self, conversation: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Ensure conversation starts with assistant message.
        If it starts with user, try to find a BOT message to pair with.
        """
        if not conversation:
            return []
        
        # If already starts with assistant, return as is
        if conversation[0]['role'] == 'assistant':
            return conversation
        
        # If starts with user, we need to find an assistant message
        # For sliding window, we might lose the pairing, so we'll try to reconstruct
        assistant_msgs = [msg for msg in conversation if msg['role'] == 'assistant']
        user_msgs = [msg for msg in conversation if msg['role'] == 'user']
        
        if not assistant_msgs:
            return []  # Can't create valid conversation without assistant
        
        # Rebuild conversation maintaining chronological order but ensuring assistant-first pairs
        result = []
        for i in range(min(len(assistant_msgs), len(user_msgs))):
            result.append(assistant_msgs[i])
            result.append(user_msgs[i])
        
        return result
    
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
                'response_time': '',  # Sẽ được fill bởi evaluator
                'context_length': conv['context_length']  # Debug: số messages trong context
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
            
            # In thống kê context length
            if 'context_length' in df.columns:
                context_stats = df['context_length'].value_counts().sort_index()
                print(f"📊 Thống kê context length:")
                for length, count in context_stats.items():
                    print(f"   - {length} messages: {count} conversations")
            
            # Xuất ra Excel
            df.to_excel(output_filepath, index=False, engine='openpyxl')
            print(f"✅ Đã xuất dữ liệu ra: {output_filepath}")
            print(f"📊 Số lượng conversations: {len(conversations)}")
            print(f"🎯 Strategy: Tối đa 3 turns (6 messages) sliding window context")
            
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
            output_filename = filename.replace('.json', '_processed_v3_3turns.xlsx')
            output_path = os.path.join('output', output_filename)
            
            print(f"\n🔄 Đang xử lý: {filename}")
            processor.process_file(input_path, output_path)

if __name__ == "__main__":
    process_all_input_files()