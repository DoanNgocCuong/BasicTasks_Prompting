import pandas as pd
import os
import glob
import re
from datetime import datetime

def extract_conversation_id(filename):
    """
    Extract conversation ID from filename
    Example: conversation_19720_output_eval.xlsx -> 19720
    """
    match = re.search(r'conversation_(\d+)_output_eval\.xlsx', filename)
    if match:
        return int(match.group(1))
    return None

def merge_all_excel_files():
    """
    Gộp tất cả file .xlsx trong folder hiện tại vào 1 sheet duy nhất
    """
    # Lấy đường dẫn folder hiện tại
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Tìm tất cả file .xlsx
    xlsx_pattern = os.path.join(current_dir, "conversation_*_output_eval.xlsx")
    xlsx_files = glob.glob(xlsx_pattern)
    
    print(f"=== BẮT ĐẦU MERGE {len(xlsx_files)} FILE EXCEL ===")
    print(f"Folder: {current_dir}")
    
    all_data = []
    error_files = []
    processed_count = 0
    
    for file_path in xlsx_files:
        try:
            filename = os.path.basename(file_path)
            
            # Extract conversation ID từ tên file
            conversation_id = extract_conversation_id(filename)
            if conversation_id is None:
                print(f"❌ Không thể extract ID từ: {filename}")
                error_files.append(filename)
                continue
            
            # Đọc file Excel
            df = pd.read_excel(file_path)
            
            # Thêm cột conversationID vào đầu
            df.insert(0, 'conversationID', conversation_id)
            
            # Thêm vào list tổng
            all_data.append(df)
            
            processed_count += 1
            
            # Log progress mỗi 50 file
            if processed_count % 50 == 0:
                print(f"✅ Đã xử lý: {processed_count}/{len(xlsx_files)} files")
                
        except Exception as e:
            print(f"❌ Lỗi khi đọc {filename}: {str(e)}")
            error_files.append(filename)
            continue
    
    if not all_data:
        print("❌ Không có data nào để merge!")
        return
    
    # Gộp tất cả DataFrame
    print(f"📊 Đang gộp {len(all_data)} DataFrames...")
    merged_df = pd.concat(all_data, ignore_index=True)
    
    # Sắp xếp theo conversationID
    merged_df = merged_df.sort_values('conversationID').reset_index(drop=True)
    
    # Tạo tên file output với timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"merged_all_conversations_{timestamp}.xlsx"
    output_path = os.path.join(current_dir, output_filename)
    
    # Lưu file
    print(f"💾 Đang lưu file: {output_filename}")
    merged_df.to_excel(output_path, index=False)
    
    # Thống kê kết quả
    print(f"\n=== KẾT QUẢ MERGE ===")
    print(f"✅ Thành công: {processed_count}/{len(xlsx_files)} files")
    print(f"❌ Lỗi: {len(error_files)} files")
    print(f"📊 Tổng rows: {len(merged_df):,}")
    print(f"📋 Tổng columns: {len(merged_df.columns)}")
    print(f"💾 File đã lưu: {output_filename}")
    
    # Hiển thị thông tin columns
    print(f"\n📝 COLUMNS:")
    for i, col in enumerate(merged_df.columns, 1):
        print(f"  {i}. {col}")
    
    # Hiển thị sample data
    print(f"\n📋 SAMPLE DATA (5 rows đầu):")
    print(merged_df.head().to_string())
    
    # Thống kê conversation IDs
    print(f"\n📈 THỐNG KÊ CONVERSATION IDs:")
    print(f"Min ID: {merged_df['conversationID'].min()}")
    print(f"Max ID: {merged_df['conversationID'].max()}")
    print(f"Unique IDs: {merged_df['conversationID'].nunique()}")
    
    if error_files:
        print(f"\n❌ CÁC FILE BỊ LỖI:")
        for error_file in error_files:
            print(f"  - {error_file}")
    
    return output_path, merged_df

if __name__ == "__main__":
    # Chạy merge
    result = merge_all_excel_files()
    
    if result:
        output_path, df = result
        print(f"\n🎉 HOÀN THÀNH! File merged: {os.path.basename(output_path)}")
    else:
        print("\n❌ MERGE THẤT BẠI!")