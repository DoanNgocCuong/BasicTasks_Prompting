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
    
    def calculate_avg_response_time(self, eval_file_path: str) -> float:
        """
        Tính response time trung bình từ file eval
        """
        try:
            if not os.path.exists(eval_file_path):
                return 0.0
                
            df = pd.read_excel(eval_file_path)
            
            # Kiểm tra xem có cột response_time không
            if 'response_time' not in df.columns:
                return 0.0
            
            # Xử lý response_time, thay thế empty string bằng 0
            response_times = df['response_time'].replace('', 0).replace(None, 0)
            
            # Convert to numeric, errors='coerce' sẽ chuyển invalid values thành NaN
            response_times = pd.to_numeric(response_times, errors='coerce').fillna(0)
            
            # Tính trung bình, bỏ qua các giá trị 0
            valid_times = response_times[response_times > 0]
            if len(valid_times) > 0:
                return round(valid_times.mean(), 2)
            else:
                return 0.0
                
        except Exception as e:
            print(f"⚠️ Lỗi khi tính avg response time cho {eval_file_path}: {e}")
            return 0.0

    def create_final_excel(self, results: list, output_file: str):
        """
        Tạo file Excel cuối cùng với mỗi ID là một sheet
        """
        print(f"\n📊 Tạo file Excel tổng hợp: {output_file}")
        
        # Tạo summary data trước (để có thể dùng trong exception)
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
        
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Tạo sheet tổng quan
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                print(f"✅ Đã tạo sheet Summary")
                
                # Tạo sheet cho từng ID
                successful_sheets = 0
                for result in results:
                    if result['eval_status'] == 'SUCCESS' and os.path.exists(result['eval_file']):
                        try:
                            df = pd.read_excel(result['eval_file'])
                            sheet_name = f"ID_{result['id']}"
                            
                            # Kiểm tra độ dài tên sheet (Excel limit 31 chars)
                            if len(sheet_name) > 31:
                                sheet_name = sheet_name[:31]
                            
                            df.to_excel(writer, sheet_name=sheet_name, index=False)
                            print(f"✅ Đã thêm sheet: {sheet_name}")
                            successful_sheets += 1
                            
                        except Exception as e:
                            print(f"❌ Lỗi khi thêm sheet cho ID {result['id']}: {e}")
                    else:
                        if result['eval_status'] == 'SUCCESS':
                            print(f"⚠️ File không tồn tại: {result['eval_file']}")
                
                print(f"📊 Tổng cộng: {successful_sheets + 1} sheets")
            
            print(f"✅ Đã tạo file tổng hợp: {output_file}")
            
        except Exception as e:
            print(f"❌ Lỗi khi tạo file Excel tổng hợp: {e}")
            print(f"🔍 Loại lỗi: {type(e).__name__}")
            
            # Tạo file backup đơn giản
            try:
                backup_file = output_file.replace('.xlsx', '_backup.csv')
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_csv(backup_file, index=False, encoding='utf-8')
                print(f"📄 Đã tạo file backup CSV: {backup_file}")
            except Exception as backup_error:
                print(f"❌ Không thể tạo backup: {backup_error}")
    
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
            avg_time = self.calculate_avg_response_time(result['eval_file']) if result['eval_status'] == 'SUCCESS' else 0
            print(f"{status_icon} ID {result['id']}: {result['eval_status']} (Avg: {avg_time}ms)")
        
        # Files được tạo
        print(f"\n📁 Files được tạo:")
        for result in results:
            if result['eval_status'] == 'SUCCESS':
                print(f"   📄 {result['eval_file']}")

def parse_arguments():
    """
    Parse command line arguments
    """
    print("🔍 DEBUG: Parsing command line arguments...")
    print(f"🔍 DEBUG: sys.argv = {sys.argv}")
    
    parser = argparse.ArgumentParser(description='Fast Response Evaluation Pipeline')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--ids', nargs='+', help='Conversation IDs (space separated)')
    group.add_argument('--id_file', type=str, help='File containing conversation IDs (one per line)')
    
    parser.add_argument('--token', type=str, default='{{token}}', 
                       help='API token (default: {{token}})')
    
    args = parser.parse_args()
    
    # Debug thông tin arguments
    print(f"🔍 DEBUG: Parsed arguments:")
    print(f"🔍 DEBUG: args.ids = {getattr(args, 'ids', None)}")
    print(f"🔍 DEBUG: args.id_file = {getattr(args, 'id_file', None)}")
    print(f"🔍 DEBUG: args.token = '{args.token}'")
    print(f"🔍 DEBUG: len(args.token) = {len(args.token) if args.token else 0}")
    
    return args

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
    print("🚀 DEBUG: Starting main function...")
    
    try:
        args = parse_arguments()
    except SystemExit as e:
        print(f"❌ DEBUG: SystemExit caught during argument parsing: {e}")
        print(f"🔍 DEBUG: Exit code: {e.code}")
        raise
    except Exception as e:
        print(f"❌ DEBUG: Exception during argument parsing: {e}")
        print(f"🔍 DEBUG: Exception type: {type(e).__name__}")
        raise
    
    print("✅ DEBUG: Arguments parsed successfully")
    
    # Validate token
    print("🔍 DEBUG: Validating token...")
    if not args.token:
        print("❌ ERROR: Token is None or empty")
        sys.exit(1)
    elif args.token == '{{token}}':
        print("⚠️ WARNING: Token appears to be a placeholder '{{token}}'")
        print("   This should be replaced with your actual API token")
        print("   Examples:")
        print("   - python main.py --ids 8532 --token your_actual_token_here")
        print("   - export TOKEN=your_token && python main.py --ids 8532 --token $TOKEN")
        # Continue anyway for testing - you may want to change this behavior
        print("   Continuing with placeholder token for debugging...")
    elif args.token.strip() == '':
        print("❌ ERROR: Token is empty or contains only whitespace")
        sys.exit(1)
    else:
        print(f"✅ DEBUG: Token appears valid (length: {len(args.token)})")
    
    # Lấy danh sách IDs
    print("🔍 DEBUG: Processing conversation IDs...")
    if args.ids:
        conversation_ids = args.ids
        print(f"✅ DEBUG: Using IDs from command line: {conversation_ids}")
    elif args.id_file:
        conversation_ids = read_ids_from_file(args.id_file)
        if not conversation_ids:
            print("❌ Không thể đọc IDs từ file")
            sys.exit(1)
        print(f"✅ DEBUG: Using IDs from file: {conversation_ids}")
    else:
        print("❌ Cần cung cấp --ids hoặc --id_file")
        sys.exit(1)
    
    # Khởi tạo và chạy pipeline
    print("🔍 DEBUG: Initializing pipeline...")
    try:
        pipeline = FastResponsePipeline(args.token)
        print("✅ DEBUG: Pipeline initialized successfully")
        pipeline.run_pipeline(conversation_ids)
    except Exception as e:
        print(f"❌ DEBUG: Error in pipeline: {e}")
        print(f"🔍 DEBUG: Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Nếu chạy trực tiếp mà không có args, dùng test IDs
    if len(sys.argv) == 1:
        print("🧪 Chế độ test với IDs mặc định")
        test_ids = ["358", "359", "362"]
        pipeline = FastResponsePipeline("{{token}}")
        pipeline.run_pipeline(test_ids)
    else:
        main()
