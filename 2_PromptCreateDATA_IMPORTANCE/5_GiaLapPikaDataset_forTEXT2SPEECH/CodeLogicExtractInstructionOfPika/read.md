tôi có 1 file excel. 
- Bạn vào từng sheet. Tìm đến ô : SYSTEM_TASK_DESCRIPTION
trong cột này tìm đến dòng đầu tiên. 

- trong dòng đầu tiên này có text bên trong. Bạn tìm đến từ: "INSTRUCTION" "instruction" "Instruction" ...
xong rồi trích ra output cho tôi  từ INSTRUCTION đến hết trong dòng đó. 

- Filename: 1. Personalized AI Coach - Thiết lập Agent.xlsx
- Output cuối trả ra 1 file excel với 1 cột: INSTRUCTION_of_SYSTEM_TASK_DESCRIPTION

---
thêm log để fix bug. 
- và cơ chế: Bỏ qua nếu sheet khong có cột 
- Bỏ qua nếu cột không có INSTRUCTION, ...