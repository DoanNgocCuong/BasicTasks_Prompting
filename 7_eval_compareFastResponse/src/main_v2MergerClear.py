"""
🚀 FAST RESPONSE EVALUATION PIPELINE WITH AUTO MERGE & CLEANUP
=============================================================

📋 MỤC ĐÍCH:
- Tự động hóa quá trình đánh giá Fast Response cho nhiều conversation IDs
- Xử lý từ A-Z: Fetch data -> Process -> Evaluate -> Merge -> Cleanup
- Tự động gộp tất cả kết quả vào 1 file Excel duy nhất
- Tự động dọn dẹp các file trung gian sau khi hoàn thành

🔄 QUY TRÌNH PIPELINE:
1. 📥 Fetch: Lấy dữ liệu conversation từ API
2. ⚙️ Process: Xử lý dữ liệu thành format chuẩn
3. 🤖 Evaluate: Đánh giá với Fast Response API
4. 📊 Merge: Gộp tất cả kết quả vào 1 file Excel
5. 🗑️ Cleanup: Xóa các file trung gian, chỉ giữ file merged

📁 CẤU TRÚC THƯ MỤC:
- input/: Dữ liệu raw từ API
- output/: Dữ liệu đã xử lý
- eval/: Kết quả đánh giá từ Fast Response API
- final/: File Excel tổng hợp cuối cùng (chỉ giữ file merged)

🎯 CÁCH SỬ DỤNG:
python main_v2MergerClear.py --ids 358 359 362 --token your_token
python main_v2MergerClear.py --id_file ids.txt --token your_token

📊 KẾT QUẢ CUỐI CÙNG:
- 1 file Excel duy nhất chứa tất cả conversation data
- Tự động có conversationID để phân biệt
- Tự động sắp xếp theo ID tăng dần
- Các file trung gian đã được dọn dẹp
"""

import sys
import argparse
import os
import pandas as pd
import glob
import re
from datetime import datetime
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
        Chạy pipeline cho danh sách conversation IDs với Auto Merge & Cleanup
        """
        print(f"🚀 Bắt đầu FULL PIPELINE với {len(conversation_ids)} conversation IDs")
        print(f"📋 Danh sách IDs: {', '.join(conversation_ids)}")
        
        results = []
        
        # Bước 1-3: Xử lý từng ID (Fetch -> Process -> Evaluate)
        print(f"\n{'='*60}")
        print(f"🔄 BƯỚC 1-3: XỬ LÝ TỪNG CONVERSATION ID")
        print(f"{'='*60}")
        
        for conv_id in conversation_ids:
            result = self.process_single_id(conv_id)
            results.append(result)
        
        # In báo cáo tóm tắt pipeline
        self.print_summary_report(results)
        
        # Bước 4: Merge tất cả file Excel thành 1 file duy nhất
        print(f"\n{'='*60}")
        print(f"📊 BƯỚC 4: MERGE TẤT CẢ FILE EXCEL")
        print(f"{'='*60}")
        
        merged_file = self.merge_all_excel_files()
        
        if merged_file:
            # Bước 5: Cleanup - Xóa tất cả file trung gian
            print(f"\n{'='*60}")
            print(f"🗑️ BƯỚC 5: CLEANUP FILE TRUNG GIAN")
            print(f"{'='*60}")
            
            self.cleanup_intermediate_files(merged_file)
            
            # In báo cáo cuối cùng
            print(f"\n{'='*60}")
            print(f"🎉 PIPELINE HOÀN THÀNH THÀNH CÔNG!")
            print(f"{'='*60}")
            print(f"📊 Tổng conversation IDs: {len(conversation_ids)}")
            print(f"✅ IDs thành công: {sum(1 for r in results if r['eval_status'] == 'SUCCESS')}")
            print(f"📁 File kết quả cuối cùng: {merged_file}")
            print(f"🗑️ Đã dọn dẹp tất cả file trung gian")
            print(f"{'='*60}")
            
        else:
            print(f"\n❌ PIPELINE THẤT BẠI: Không thể merge files!")
        
        return results, merged_file if merged_file else None
    
    def extract_conversation_id(self, filename: str) -> int:
        """
        Extract conversation ID from filename
        Example: conversation_19720_output_eval.xlsx -> 19720
        """
        match = re.search(r'conversation_(\d+)_output_eval\.xlsx', filename)
        if match:
            return int(match.group(1))
        return None

    def count_xlsx_files(self, folder_path: str) -> tuple:
        """
        Đếm số file .xlsx trong folder chỉ định
        """
        xlsx_pattern = os.path.join(folder_path, "*.xlsx")
        xlsx_files = glob.glob(xlsx_pattern)
        count = len(xlsx_files)
        
        print(f"📊 THỐNG KÊ FILE XLSX - {os.path.basename(folder_path)}/")
        print(f"   Số file .xlsx: {count}")
        
        if count > 0:
            total_size = sum(os.path.getsize(f) for f in xlsx_files)
            print(f"   Tổng dung lượng: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
        
        return count, xlsx_files

    def merge_all_excel_files(self) -> str:
        """
        Gộp tất cả file evaluation Excel vào 1 file duy nhất
        """
        print(f"\n{'='*60}")
        print(f"📊 BẮT ĐẦU MERGE TẤT CẢ FILE EXCEL")
        print(f"{'='*60}")
        
        # Tìm tất cả file conversation_*_output_eval.xlsx trong folder eval/
        eval_pattern = os.path.join("eval", "conversation_*_output_eval.xlsx")
        xlsx_files = glob.glob(eval_pattern)
        
        # Debug: Hiển thị tất cả files được tìm thấy
        print(f"🔍 DEBUG: Pattern tìm kiếm: {eval_pattern}")
        print(f"🔍 DEBUG: Số file tìm thấy: {len(xlsx_files)}")
        
        if xlsx_files:
            print(f"📁 Danh sách files tìm thấy:")
            for i, file_path in enumerate(xlsx_files, 1):
                filename = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                print(f"   {i}. {filename} ({file_size:,} bytes)")
        else:
            # Debug: Kiểm tra folder eval/ có tồn tại không
            if not os.path.exists("eval"):
                print("❌ Folder eval/ không tồn tại!")
            else:
                # Liệt kê tất cả files trong eval/
                all_files = os.listdir("eval")
                print(f"🔍 DEBUG: Folder eval/ có {len(all_files)} files:")
                for f in all_files:
                    print(f"   - {f}")
            return None
        
        print(f"📁 Tìm thấy {len(xlsx_files)} file để merge từ eval/")
        
        all_data = []
        error_files = []
        processed_count = 0
        
        for file_path in xlsx_files:
            try:
                filename = os.path.basename(file_path)
                
                # Extract conversation ID từ tên file
                conversation_id = self.extract_conversation_id(filename)
                if conversation_id is None:
                    print(f"❌ Không thể extract ID từ: {filename}")
                    error_files.append(filename)
                    continue
                
                # Đọc file Excel
                df = pd.read_excel(file_path)
                
                # Debug: Hiển thị thông tin DataFrame
                if processed_count == 0:  # Chỉ show info của file đầu tiên
                    print(f"🔍 DEBUG: Cấu trúc file đầu tiên ({filename}):")
                    print(f"   - Rows: {len(df)}")
                    print(f"   - Columns: {len(df.columns)}")
                    print(f"   - Column names: {list(df.columns)}")
                    if len(df) > 0:
                        print(f"   - Sample data (first row): {df.iloc[0].to_dict()}")
                
                # Thêm cột conversationID vào đầu
                df.insert(0, 'conversationID', conversation_id)
                
                # Thêm vào list tổng
                all_data.append(df)
                processed_count += 1
                
                # Log progress mỗi 20 file
                if processed_count % 20 == 0:
                    print(f"✅ Đã xử lý: {processed_count}/{len(xlsx_files)} files")
                    
            except Exception as e:
                print(f"❌ Lỗi khi đọc {filename}: {str(e)}")
                error_files.append(filename)
                continue
        
        if not all_data:
            print("❌ Không có data nào để merge!")
            return None
        
        # Validation: Kiểm tra tất cả file có cùng columns không
        print(f"🔍 DEBUG: Validating column consistency...")
        all_columns = [list(df.columns) for df in all_data]
        first_columns = all_columns[0]
        
        column_mismatch = False
        for i, cols in enumerate(all_columns[1:], 1):
            if cols != first_columns:
                print(f"⚠️ WARNING: File {i+1} có columns khác: {cols}")
                column_mismatch = True
        
        if not column_mismatch:
            print(f"✅ Tất cả {len(all_data)} files có cùng column structure")
        
        # Gộp tất cả DataFrame
        print(f"📊 Đang gộp {len(all_data)} DataFrames...")
        try:
            merged_df = pd.concat(all_data, ignore_index=True)
            print(f"✅ Concat thành công!")
        except Exception as e:
            print(f"❌ Lỗi khi concat DataFrames: {e}")
            return None
        
        # Sắp xếp theo conversationID
        print(f"📈 Đang sắp xếp theo conversationID...")
        merged_df = merged_df.sort_values('conversationID').reset_index(drop=True)
        
        # Debug: Thông tin về merged DataFrame
        print(f"🔍 DEBUG: Merged DataFrame info:")
        print(f"   - Total rows: {len(merged_df):,}")
        print(f"   - Total columns: {len(merged_df.columns)}")
        print(f"   - Columns: {list(merged_df.columns)}")
        print(f"   - ConversationID range: {merged_df['conversationID'].min()} - {merged_df['conversationID'].max()}")
        print(f"   - Unique conversations: {merged_df['conversationID'].nunique()}")
        
        # Tạo tên file output với timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"merged_all_conversations_{timestamp}.xlsx"
        output_path = os.path.join("final", output_filename)
        
        # Lưu file
        print(f"💾 Đang lưu file: {output_filename}")
        try:
            merged_df.to_excel(output_path, index=False)
            print(f"✅ Lưu file thành công!")
        except Exception as e:
            print(f"❌ Lỗi khi lưu file: {e}")
            return None
        
        # Thống kê kết quả
        print(f"\n📊 KẾT QUẢ MERGE:")
        print(f"✅ Thành công: {processed_count}/{len(xlsx_files)} files")
        print(f"❌ Lỗi: {len(error_files)} files")
        print(f"📊 Tổng rows: {len(merged_df):,}")
        print(f"📋 Tổng columns: {len(merged_df.columns)}")
        print(f"💾 File đã lưu: {output_path}")
        
        # Thống kê conversation IDs
        print(f"\n📈 THỐNG KÊ CONVERSATION IDs:")
        print(f"   Min ID: {merged_df['conversationID'].min()}")
        print(f"   Max ID: {merged_df['conversationID'].max()}")
        print(f"   Unique IDs: {merged_df['conversationID'].nunique()}")
        
        if error_files:
            print(f"\n❌ CÁC FILE BỊ LỖI:")
            for error_file in error_files:
                print(f"   - {error_file}")
        
        return output_path

    def cleanup_intermediate_files(self, keep_merged_file: str):
        """
        Xóa tất cả file trung gian, chỉ giữ lại file merged
        """
        print(f"\n{'='*60}")
        print(f"🗑️ BẮT ĐẦU DỌN DẸP FILE TRUNG GIAN")
        print(f"{'='*60}")
        
        folders_to_clean = ['input', 'output', 'eval']
        total_deleted = 0
        total_size_freed = 0
        
        for folder in folders_to_clean:
            if not os.path.exists(folder):
                continue
                
            print(f"\n🗂️ Dọn dẹp folder: {folder}/")
            
            # Đếm files trước khi xóa
            count, files = self.count_xlsx_files(folder)
            if count == 0:
                print(f"   ✨ Folder đã sạch!")
                continue
            
            # Xóa tất cả files trong folder
            deleted_count = 0
            for file_path in files:
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    deleted_count += 1
                    total_deleted += 1
                    total_size_freed += file_size
                    print(f"   🗑️ Đã xóa: {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"   ❌ Không xóa được {os.path.basename(file_path)}: {e}")
            
            print(f"   ✅ Đã xóa {deleted_count}/{count} files")
        
        # Dọn dẹp folder final, chỉ giữ file merged mới nhất
        print(f"\n🗂️ Dọn dẹp folder: final/")
        if os.path.exists("final"):
            final_files = glob.glob(os.path.join("final", "*.xlsx"))
            kept_file = os.path.basename(keep_merged_file)
            
            deleted_in_final = 0
            for file_path in final_files:
                if os.path.basename(file_path) != kept_file:
                    try:
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        deleted_in_final += 1
                        total_deleted += 1
                        total_size_freed += file_size
                        print(f"   🗑️ Đã xóa: {os.path.basename(file_path)}")
                    except Exception as e:
                        print(f"   ❌ Không xóa được {os.path.basename(file_path)}: {e}")
            
            if deleted_in_final == 0:
                print(f"   ✨ Chỉ có file merged, không cần xóa!")
            else:
                print(f"   ✅ Đã xóa {deleted_in_final} file cũ")
        
        print(f"\n🎯 KẾT QUẢ DỌN DẸP:")
        print(f"   🗑️ Tổng files đã xóa: {total_deleted}")
        print(f"   💾 Dung lượng giải phóng: {total_size_freed:,} bytes ({total_size_freed/1024/1024:.2f} MB)")
        print(f"   📁 File được giữ lại: {keep_merged_file}")

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
        
        results, merged_file = pipeline.run_pipeline(conversation_ids)
        
        if merged_file:
            print(f"\n🎉 SUCCESS: Pipeline completed successfully!")
            print(f"📁 Final merged file: {merged_file}")
        else:
            print(f"\n⚠️ WARNING: Pipeline completed but merge failed!")
            
    except Exception as e:
        print(f"❌ DEBUG: Error in pipeline: {e}")
        print(f"🔍 DEBUG: Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Nếu chạy trực tiếp mà không có args, dùng test IDs
    if len(sys.argv) == 1:
        print("🧪 CHẠY CHẾ ĐỘ TEST VỚI IDs MẶC ĐỊNH")
        print("=" * 60)
        test_ids = ["358", "359", "362"]
        
        try:
            pipeline = FastResponsePipeline("{{token}}")
            results, merged_file = pipeline.run_pipeline(test_ids)
            
            if merged_file:
                print(f"\n🎉 TEST THÀNH CÔNG!")
                print(f"📁 File merged: {merged_file}")
            else:
                print(f"\n❌ TEST THẤT BẠI: Không merge được!")
                
        except Exception as e:
            print(f"\n❌ LỖI TRONG TEST: {e}")
            import traceback
            traceback.print_exc()
    else:
        main()
