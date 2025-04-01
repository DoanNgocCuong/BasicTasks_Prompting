import re
import pandas as pd
import logging

# Cấu hình logging: mức DEBUG để hiển thị tất cả các log, bao gồm debug, info, warning, error
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Đường dẫn file Excel đầu vào
input_file = "output_data_v2.xlsx"
logging.info(f"Đang đọc file input: {input_file}")

# Đọc file Excel
try:
    df_input = pd.read_excel(input_file)
    logging.info(f"Đã đọc file thành công. Số dòng đọc được: {df_input.shape[0]}")
except Exception as e:
    logging.error(f"Lỗi khi đọc file Excel: {e}")
    raise e

# Kiểm tra sự tồn tại của cột 'assistant_response'
if 'assistant_response' not in df_input.columns:
    logging.error("Cột 'assistant_response' không tồn tại trong file Excel!")
    raise KeyError("Cột 'assistant_response' không tồn tại trong file Excel!")

# Biểu thức chính quy để parse cụm từ:
# Pattern 1: Cho dạng số 1. 2. 3.
# Pattern 2: Cho dạng xuống dòng bình thường
pattern_numbered = r'\d+\.\s*(.*?)\s*(?=\d+\.|$)'
pattern_newline = r'([^\n]+)'

phrases = []

# Duyệt qua từng dòng của cột 'assistant_response'
for idx, text in enumerate(df_input['assistant_response']):
    logging.debug(f"Xử lý dòng {idx}: {text}")
    if isinstance(text, str):
        # Thử tìm matches với pattern số
        matches_numbered = re.findall(pattern_numbered, text)
        
        if matches_numbered:
            logging.debug(f"Dòng {idx}: Tìm thấy {len(matches_numbered)} cụm từ dạng số.")
            phrases.extend(matches_numbered)
        else:
            # Nếu không tìm thấy dạng số, thử tìm theo dòng
            matches_newline = re.findall(pattern_newline, text)
            if matches_newline:
                logging.debug(f"Dòng {idx}: Tìm thấy {len(matches_newline)} cụm từ dạng dòng.")
                # Lọc bỏ các dòng trống
                valid_matches = [match.strip() for match in matches_newline if match.strip()]
                phrases.extend(valid_matches)
            else:
                logging.warning(f"Dòng {idx}: Không tìm thấy cụm từ nào.")
    else:
        logging.warning(f"Dòng {idx}: Giá trị không phải chuỗi. Giá trị: {text}")

logging.info(f"Tổng số cụm từ được trích xuất: {len(phrases)}")

# Tạo DataFrame mới chứa các cụm từ đã được parse
df_output = pd.DataFrame(phrases, columns=["Phrase"])
logging.debug("DataFrame đầu ra đã được tạo với cột 'Phrase'.")

# Đường dẫn file Excel đầu ra
output_file = "output_data_v2_output.xlsx"
try:
    df_output.to_excel(output_file, index=False)
    logging.info(f"Đã tạo file Excel '{output_file}' thành công với {len(df_output)} dòng.")
except Exception as e:
    logging.error(f"Lỗi khi xuất file Excel: {e}")
    raise e

print(f"Đã tạo file Excel '{output_file}' thành công!")
