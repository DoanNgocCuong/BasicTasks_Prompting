import sys
import argparse
import os
import pandas as pd
from get_data_conversation import ConversationDataFetcher
from processed import ConversationProcessor
from run_eval_api_fast_response import FastResponseEvaluator

class FastResponsePipeline:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.fetcher = ConversationDataFetcher(api_token)
        self.processor = ConversationProcessor()
        self.evaluator = FastResponseEvaluator()
        
        # Tạo các folder cần thiết
        for folder in ['input', 'output', 'eval', 'final']:
            if not os.path.exists(folder):
                os.makedirs(folder)
    
    def process_single_id(self, conversation_id: str) -> dict:
        """
        Xử lý một conversation ID
        """
        print(f"\n{'='*50}")
        print(f"🔄 Bắt đầu xử lý conversation ID: {conversation_id}")
        print(f"{'='*50}")
        
        results = {
            'id': conversation_id,
            'fetch_status': 'FAILED',
            'process_status': 'FAILED',
            'eval_status': 'FAILED',
            'input_file': '',
            'processed_file': '',
            'eval_file': ''
        }
        
        # Bước 1: Lấy dữ liệu
        print(f"📥 Bước 1: Lấy dữ liệu từ API...")
        input_file = self.fetcher.fetch_and_save(conversation_id)
        if input_file:
            results['fetch_status'] = 'SUCCESS'
            results['input_file'] = input_file
        else:
            print(f"❌ Không thể lấy dữ liệu cho ID: {conversation_id}")
            return results
        
        # Bước 2: Xử lý dữ liệu
        print(f"⚙️ Bước 2: Xử lý dữ liệu...")
        processed_file = f"output/conversation_{conversation_id}_processed.xlsx"
        if self.processor.process_file(input_file, processed_file):
            results['process_status'] = 'SUCCESS'
            results['processed_file'] = processed_file
        else:
            print(f"❌ Không thể xử lý dữ liệu cho ID: {conversation_id}")
            return results
        
        # Bước 3: Đánh giá với API
        print(f"🤖 Bước 3: Đánh giá với Fast Response API...")
        eval_file = f"eval/conversation_{conversation_id}_output_eval.xlsx"
        if self.evaluator.evaluate_excel_file(processed_file, eval_file):
            results['eval_status'] = 'SUCCESS'
            results['eval_file'] = eval_file
        else:
            print(f"❌ Không thể đánh giá cho ID: {conversation_id}")
            return results
        
        print(f"✅ Hoàn thành xử lý ID: {conversation_id}")
        return results
    
    def create_final_excel(self, results: list, output_file: str):
        """
        Tạo file Excel cuối cùng với mỗi ID là một sheet
        """
        print(f"\n📊 Tạo file Excel tổng hợp: {output_file}")
        
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Tạo sheet tổng quan
                summary_data = []
                for result in results:
                    summary_data.append({
                        'ID': result['id'],
                        'Fetch Status': result['fetch_status'],
                        'Process Status': result['process_status'],
                        'Eval Status': result['eval_status'],
                        'Input File': result['input_file'],
                        'Processed File': result['processed_file'],
                        'Eval File': result['eval_file'],
                        'Avg Response Time (ms)': self.calculate_avg_response_time(result['eval_file']) if result['eval_status'] == 'SUCCESS' else 0
                    })
                
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Tạo sheet cho từng ID
                for result in results:
                    if result['eval_status'] == 'SUCCESS' and os.path.exists(result['eval_file']):
                        try:
                            df = pd.read_excel(result['eval_file'])
                            sheet_name = f"ID_{result['id']}"
                            df.to_excel(writer, sheet_name=sheet_name, index=False)
                            print(f"✅ Đã thêm sheet: {sheet_name}")
                        except Exception as e:
                            print(f"❌ Lỗi khi thêm sheet cho ID {result['id']}: {e}")
            
            print(f"✅ Đã tạo file tổng hợp: {output_file}")
            
        except Exception as e:
            print(f"❌ Lỗi khi tạo file Excel tổng hợp: {e}")
            # Tạo file backup đơn giản
            backup_file = output_file.replace('.xlsx', '_backup.csv')
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_csv(backup_file, index=False, encoding='utf-8')
            print(f"📄 Đã tạo file backup CSV: {backup_file}")
    
    def run_pipeline(self, conversation_ids: list):
        """
        Chạy pipeline cho danh sách conversation IDs
        """
        print(f"🚀 Bắt đầu pipeline với {len(conversation_ids)} conversation IDs")
        print(f"📋 Danh sách IDs: {', '.join(conversation_ids)}")
        
        results = []
        
        for conv_id in conversation_ids:
            result = self.process_single_id(conv_id)
            results.append(result)
        
        # Tạo file Excel tổng hợp
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        final_file = f"final/fast_response_evaluation_{timestamp}.xlsx"
        self.create_final_excel(results, final_file)
        
        # In báo cáo tóm tắt
        self.print_summary_report(results)
        
        return results
    
    def print_summary_report(self, results: list):
        """
        In báo cáo tóm tắt
        """
        print(f"\n{'='*60}")
        print(f"📊 BÁO CÁO TÓM TẮT")
        print(f"{'='*60}")
        
        total = len(results)
        success_fetch = sum(1 for r in results if r['fetch_status'] == 'SUCCESS')
        success_process = sum(1 for r in results if r['process_status'] == 'SUCCESS')
        success_eval = sum(1 for r in results if r['eval_status'] == 'SUCCESS')
        
        print(f"📈 Tổng số IDs xử lý: {total}")
        print(f"📥 Fetch thành công: {success_fetch}/{total} ({success_fetch/total*100:.1f}%)")
        print(f"⚙️ Process thành công: {success_process}/{total} ({success_process/total*100:.1f}%)")
        print(f"🤖 Eval thành công: {success_eval}/{total} ({success_eval/total*100:.1f}%)")
        
        # Chi tiết từng ID
        print(f"\n📋 Chi tiết từng ID:")
        for result in results:
            status_icon = "✅" if result['eval_status'] == 'SUCCESS' else "❌"
            print(f"{status_icon} ID {result['id']}: {result['eval_status']}")
        
        # Files được tạo
        print(f"\n📁 Files được tạo:")
        for result in results:
            if result['eval_status'] == 'SUCCESS':
                print(f"   📄 {result['eval_file']}")

def parse_arguments():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='Fast Response Evaluation Pipeline')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--ids', nargs='+', help='Conversation IDs (space separated)')
    group.add_argument('--id_file', type=str, help='File containing conversation IDs (one per line)')
    
    parser.add_argument('--token', type=str, default='{{token}}', 
                       help='API token (default: {{token}})')
    
    return parser.parse_args()

def read_ids_from_file(filepath: str) -> list:
    """
    Đọc IDs từ file
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            ids = [line.strip() for line in f if line.strip()]
        return ids
    except Exception as e:
        print(f"❌ Lỗi khi đọc file {filepath}: {e}")
        return []

def main():
    """
    Hàm main
    """
    args = parse_arguments()
    
    # Lấy danh sách IDs
    if args.ids:
        conversation_ids = args.ids
    elif args.id_file:
        conversation_ids = read_ids_from_file(args.id_file)
        if not conversation_ids:
            print("❌ Không thể đọc IDs từ file")
            sys.exit(1)
    else:
        print("❌ Cần cung cấp --ids hoặc --id_file")
        sys.exit(1)
    
    # Khởi tạo và chạy pipeline
    pipeline = FastResponsePipeline(args.token)
    pipeline.run_pipeline(conversation_ids)

if __name__ == "__main__":
    # Nếu chạy trực tiếp mà không có args, dùng test IDs
    if len(sys.argv) == 1:
        print("🧪 Chế độ test với IDs mặc định")
        test_ids = ["358", "359", "362"]
        pipeline = FastResponsePipeline("{{token}}")
        pipeline.run_pipeline(test_ids)
    else:
        main()
