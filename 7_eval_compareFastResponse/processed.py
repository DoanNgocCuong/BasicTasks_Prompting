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
        Mỗi conversation chứa tối đa 3 cặp BOT-USER gần nhất (6 messages).
        Sliding window theo PAIRS để maintain proper chronology.
        """
        if 'data' not in data:
            print("❌ Không tìm thấy key 'data' trong JSON")
            return []

        conversations = []
        pairs = []  # Store completed BOT-USER pairs
        MAX_TURNS = 3  # Tối đa 3 turns (3 pairs = 6 messages)
        
        # Step 1: Extract all BOT-USER pairs in chronological order
        current_bot_messages = []  # Store consecutive BOT messages
        original_data = data['data']
        
        for i, item in enumerate(original_data):
            character = item.get('character', '')
            content = item.get('content', '').strip()
            
            if not content:
                continue
                
            if character == 'BOT_RESPONSE_CONVERSATION':
                # Collect consecutive BOT messages
                current_bot_messages.append(content)
            elif character == 'USER':
                # Create pair when we have BOT messages and USER
                if current_bot_messages:
                    # Combine all consecutive BOT messages with space separation
                    combined_bot = ' '.join(current_bot_messages)
                    
                    # Find next responses after this USER
                    next_fast_response = ""
                    next_bot_response = ""
                    
                    # Find FAST_RESPONSE after this USER
                    for j in range(i+1, len(original_data)):
                        next_item = original_data[j]
                        if next_item.get('character') == 'FAST_RESPONSE':
                            next_content = next_item.get('content', '').strip()
                            if next_content:
                                next_fast_response = next_content
                                break
                    
                    # Find next BOT_RESPONSE_CONVERSATION
                    for j in range(i+1, len(original_data)):
                        next_item = original_data[j]
                        if next_item.get('character') == 'BOT_RESPONSE_CONVERSATION':
                            next_content = next_item.get('content', '').strip()
                            if next_content:
                                next_bot_response = next_content
                                break
                    
                    # Create pair and add to pairs list
                    pair = {
                        'bot': combined_bot,
                        'user': content,
                        'next_fast_response': next_fast_response,
                        'next_bot_response': next_bot_response
                    }
                    pairs.append(pair)
                    current_bot_messages = []  # Reset for next pair
                else:
                    # USER without preceding BOT - try to find BOT after
                    next_bot_messages = []
                    
                    # Collect all consecutive BOT messages after this USER
                    for j in range(i+1, len(original_data)):
                        next_item = original_data[j]
                        if next_item.get('character') == 'BOT_RESPONSE_CONVERSATION':
                            next_content = next_item.get('content', '').strip()
                            if next_content:
                                next_bot_messages.append(next_content)
                        elif next_item.get('character') == 'USER':
                            # Stop collecting when we hit another USER
                            break
                    
                    if next_bot_messages:
                        combined_next_bot = ' '.join(next_bot_messages)
                        
                        # Find responses after this USER
                        next_fast_response = ""
                        next_bot_response = ""
                        
                        for j in range(i+1, len(original_data)):
                            next_item = original_data[j]
                            if next_item.get('character') == 'FAST_RESPONSE':
                                next_content = next_item.get('content', '').strip()
                                if next_content:
                                    next_fast_response = next_content
                                    break
                        
                        # Find BOT_RESPONSE after the collected next_bot_messages
                        bot_found_count = 0
                        for j in range(i+1, len(original_data)):
                            next_item = original_data[j]
                            if next_item.get('character') == 'BOT_RESPONSE_CONVERSATION':
                                bot_found_count += 1
                                if bot_found_count > len(next_bot_messages):
                                    # This is a BOT after our collected messages
                                    next_content = next_item.get('content', '').strip()
                                    if next_content:
                                        next_bot_response = next_content
                                        break
                        
                        pair = {
                            'bot': combined_next_bot,  # Combined BOT messages after USER
                            'user': content,
                            'next_fast_response': next_fast_response,
                            'next_bot_response': next_bot_response
                        }
                        pairs.append(pair)
        
        # Step 2: Build conversations with sliding window of pairs
        for i in range(len(pairs)):
            # Get sliding window of pairs (max MAX_TURNS pairs)
            start_idx = max(0, i - MAX_TURNS + 1)
            window_pairs = pairs[start_idx:i+1]
            
            # Convert pairs to conversation format
            conversation = []
            for pair in window_pairs:
                conversation.append({"role": "assistant", "content": pair['bot']})
                conversation.append({"role": "user", "content": pair['user']})
            
            # Use the last pair's response info
            last_pair = pairs[i]
            conversations.append({
                'conversation': conversation,
                'next_fast_response': last_pair['next_fast_response'],
                'next_bot_response': last_pair['next_bot_response'],
                'context_length': len(conversation)
            })
        
        return conversations
    
    def _ensure_assistant_first(self, conversation: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Ensure conversation starts with assistant message.
        Maintain exact chronological order, just reorder if needed.
        """
        if not conversation:
            return []
        
        # If already starts with assistant, return as is
        if conversation[0]['role'] == 'assistant':
            return conversation
        
        # If starts with user, we need to move first assistant to front
        assistant_msgs = [msg for msg in conversation if msg['role'] == 'assistant']
        
        if not assistant_msgs:
            return []  # Can't create valid conversation without assistant
        
        # Strategy: Keep chronological order but ensure assistant-first
        # Find the first assistant and move it to front if needed
        result = conversation.copy()
        
        # If conversation starts with user, try to reorder smartly
        if result[0]['role'] == 'user':
            # Find first assistant
            first_assistant_idx = -1
            for i, msg in enumerate(result):
                if msg['role'] == 'assistant':
                    first_assistant_idx = i
                    break
            
            if first_assistant_idx > 0:
                # Move first assistant to front
                assistant_msg = result.pop(first_assistant_idx)
                result.insert(0, assistant_msg)
        
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