import pandas as pd
import requests
import json
import time
from typing import Dict, List, Any
import os

class FastResponseEvaluator:
    def __init__(self):
        self.api_url = "http://103.253.20.30:8990/fast_response/generate"
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def call_fast_response_api(self, conversations: List[Dict[str, str]]) -> str:
        """
        Gọi API fast response
        """
        payload = {
            "conversations": conversations,
            "system_prompt": "You are QuickReact: detect the emotion in the latest message and reply instantly in its same language (English or Vietnamese) using 1-8 words (≤60 chars), keep it short enough with a friendly informal tone that mirrors and empathizes with that feeling (sad → soothe, happy → cheer, worried → reassure; emojis/!/? welcome); output only that text—never answer the question, just buy time until the main reply arrives.",
            "model_name": "Qwen/Qwen3-4B",
            "temperature": 0.8,
            "top_p": 1
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            # Giả sử API trả về response trong field 'content' hoặc tương tự
            if isinstance(result, dict):
                return result.get('response', result.get('content', str(result)))
            return str(result)
            
        except requests.exceptions.Timeout:
            print("⏰ API timeout")
            return "API_TIMEOUT"
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return f"API_ERROR: {str(e)}"
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return f"ERROR: {str(e)}"
    
    def parse_conversation_string(self, conv_str: str) -> List[Dict[str, str]]:
        """
        Parse conversation string thành list
        """
        try:
            return json.loads(conv_str)
        except json.JSONDecodeError:
            print(f"❌ Lỗi parse conversation: {conv_str[:100]}...")
            return []
    
    def evaluate_excel_file(self, input_filepath: str, output_filepath: str) -> bool:
        """
        Đánh giá file Excel và tạo file output
        """
        try:
            # Đọc file Excel
            df = pd.read_excel(input_filepath)
            print(f"📊 Đã đọc {len(df)} rows từ {input_filepath}")
            
            # Thêm cột generated_ai
            df['generated_ai'] = ''
            
            # Xử lý từng row
            for index, row in df.iterrows():
                print(f"🔄 Đang xử lý row {index + 1}/{len(df)}")
                
                conv_str = row['BOT_RESPONSE_CONVERSATION_with_USER']
                conversations = self.parse_conversation_string(conv_str)
                
                if conversations:
                    # Gọi API
                    generated_response = self.call_fast_response_api(conversations)
                    df.at[index, 'generated_ai'] = generated_response
                    
                    # Delay để tránh spam API
                    time.sleep(0.5)
                else:
                    df.at[index, 'generated_ai'] = "PARSE_ERROR"
                
                # In progress mỗi 10 rows
                if (index + 1) % 10 == 0:
                    print(f"✅ Đã hoàn thành {index + 1}/{len(df)} rows")
            
            # Lưu file output
            df.to_excel(output_filepath, index=False, engine='openpyxl')
            print(f"✅ Đã lưu kết quả ra: {output_filepath}")
            
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi đánh giá file: {e}")
            return False
    
    def evaluate_all_processed_files(self):
        """
        Đánh giá tất cả file processed trong folder output
        """
        if not os.path.exists('output'):
            print("❌ Folder 'output' không tồn tại")
            return
        
        # Tạo folder eval nếu chưa có
        if not os.path.exists('eval'):
            os.makedirs('eval')
        
        for filename in os.listdir('output'):
            if filename.endswith('_processed.xlsx'):
                input_path = os.path.join('output', filename)
                output_filename = filename.replace('_processed.xlsx', '_output_eval.xlsx')
                output_path = os.path.join('eval', output_filename)
                
                print(f"\n🔄 Đang đánh giá: {filename}")
                self.evaluate_excel_file(input_path, output_path)

if __name__ == "__main__":
    evaluator = FastResponseEvaluator()
    evaluator.evaluate_all_processed_files()
