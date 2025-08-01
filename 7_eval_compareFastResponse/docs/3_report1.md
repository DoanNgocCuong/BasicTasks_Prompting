Em summary lại xíu: 
Chị Trang comment: 
Option 1 (hiện tại): câu fast_response đang có cảm thán trong đó. => Em đem đi fine tune trước, ngon, thì sẽ chỉnh sửa main_answer để bỏ đi câu cảm thán.Option 2 fast_response trung tính hơn. +, Nếu nhanh: tuning prompt để có fast_response trung tính hơn. 
+, Nếu lâu quá, thì trong thời gian finetune Option 1: chỉnh prompt để fast_response trung tính hơn. 
Anh Cường comment: 
20% tổng số fast-response là được mention lại ý của users chỉ khi đúng intent (trả lời đúng), ví dụ "tớ thích voi" --> "ồ voi à, tớ cũng rất thích voi" 
---=> Next steps: 1. Em đưa ver 1 đi finetune trước (cắm máy) 2. Trong thời gian đó: tuning thêm ver2 với 2 tiêu chí : TRUNG TÍNH + MENTION LẠI INTENT USER - Gửi lại anh chị đánh giá ạ. 
Anh  @Cuong Vu Cao  , chị  @Trang Nguyen Thu  