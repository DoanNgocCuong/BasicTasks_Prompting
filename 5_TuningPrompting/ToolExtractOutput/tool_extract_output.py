import re
import pandas as pd
import logging

# Cấu hình logging: mức DEBUG để hiển thị tất cả các log, bao gồm debug, info, warning, error
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Đường dẫn file Excel đầu vào
input_file = "results.xlsx"
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
# - \d+\.: khớp với số thứ tự và dấu chấm (ví dụ "1.")
# - \s*: bỏ qua khoảng trắng sau dấu chấm
# - (.*?): nhóm chứa nội dung cụm từ (non-greedy)
# - \s*(?=\d+\.|$): dừng lại khi gặp số thứ tự mới hoặc hết dòng
pattern = r'\d+\.\s*(.*?)\s*(?=\d+\.|$)'

phrases = []

# Duyệt qua từng dòng của cột 'assistant_response'
for idx, text in enumerate(df_input['assistant_response']):
    logging.debug(f"Xử lý dòng {idx}: {text}")
    if isinstance(text, str):
        matches = re.findall(pattern, text)
        if matches:
            logging.debug(f"Dòng {idx}: Tìm thấy {len(matches)} cụm từ.")
            phrases.extend(matches)
        else:
            logging.warning(f"Dòng {idx}: Không tìm thấy cụm từ nào với pattern đã cho.")
    else:
        logging.warning(f"Dòng {idx}: Giá trị không phải chuỗi. Giá trị: {text}")

logging.info(f"Tổng số cụm từ được trích xuất: {len(phrases)}")

# Tạo DataFrame mới chứa các cụm từ đã được parse
df_output = pd.DataFrame(phrases, columns=["Phrase"])
logging.debug("DataFrame đầu ra đã được tạo với cột 'Phrase'.")

# Đường dẫn file Excel đầu ra
output_file = "output.xlsx"
try:
    df_output.to_excel(output_file, index=False)
    logging.info(f"Đã tạo file Excel '{output_file}' thành công với {len(df_output)} dòng.")
except Exception as e:
    logging.error(f"Lỗi khi xuất file Excel: {e}")
    raise e

print(f"Đã tạo file Excel '{output_file}' thành công!")
