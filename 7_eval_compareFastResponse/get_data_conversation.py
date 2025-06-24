import requests
import json
import os
from typing import Optional

class ConversationDataFetcher:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://robot-api.hacknao.edu.vn/robot/api/v1/admin/conversations"
        self.headers = {
            'X-API-Key': api_token,
            'accept': 'application/json'
        }
        
        # Tạo folder input nếu chưa có
        if not os.path.exists('input'):
            os.makedirs('input')
    
    def fetch_conversation(self, conversation_id: str) -> Optional[dict]:
        """
        Lấy dữ liệu conversation từ API
        """
        url = f"{self.base_url}/{conversation_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            print(f"✅ Lấy dữ liệu thành công cho conversation ID: {conversation_id}")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi khi lấy dữ liệu cho conversation ID {conversation_id}: {e}")
            return None
    
    def save_to_file(self, conversation_id: str, data: dict) -> str:
        """
        Lưu dữ liệu vào file JSON
        """
        filename = f"input/conversation_{conversation_id}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Đã lưu dữ liệu vào: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Lỗi khi lưu file {filename}: {e}")
            return ""
    
    def fetch_and_save(self, conversation_id: str) -> str:
        """
        Lấy và lưu dữ liệu conversation
        """
        data = self.fetch_conversation(conversation_id)
        if data:
            return self.save_to_file(conversation_id, data)
        return ""

if __name__ == "__main__":
    # Test với token mẫu
    TOKEN = "{{token}}"  # Thay thế bằng token thực
    
    fetcher = ConversationDataFetcher(TOKEN)
    
    # Test với ID mẫu
    test_ids = ["8532", "358", "359", "362"]
    
    for conv_id in test_ids:
        print(f"\n🔄 Đang xử lý conversation ID: {conv_id}")
        fetcher.fetch_and_save(conv_id)
