Tool: GPTs/Chạy hàng loạt các dòng trong file excel
1. Testing Response LLM
1.1 [QA Benchmark Testing] Với từng file trong 5 file: Tính năng 1, 2, 3, 4 và file Mapping - gen = GPT web
Đúc kết các đầu mục chính của PDF này (Tiếng Việt)
- NHÓM TEST 1: Tạo 5 FAQs về nội dung tổng quan => 5 câu
RESPONSE dạng bảng: câu hỏi, câu trả lời
- NHÓM TEST 2: Với mỗi mục lớn, tạo 5 câu hỏi chuẩn để test LLMs=> 9 mục * 5 = 45 câu 
Respone dạng bảng : mục lớn - câu hỏi chuẩn - câu trả lời
- NHÓM TEST 3: Với mỗi mục lớn, tạo 5 câu hỏi mơ hồ để test LLMs (câu trả lời vẫn rõ ràng) => 9 mục * 5 = 45 câu  Respone dạng bảng : mục lớn - câu hỏi mơ hồ - câu trả lời
- NHÓM TEST 4: 1 file 9 mục chính, mỗi mục 16 câu. => 1 file 9 mục * 16 = ... câu

- Chi tiết NHÓM TEST 4: 
+, Chú ý: CHỈ SỬ DỤNG NỘI DUNG trong file đã tải lên ĐỂ TẠO CÂU HỎI. Đọc to tên file và nhắn "rõ" nếu bạn đã hiểu chỉ sử dụng nội dung trong file để tạo câu hỏi
+, Với từng đề mục lớn trong các đề mục lớn đã tóm tắt bên trên. 
 Bắt đầu từ đề mục lớn: """ 1. Insight: Phát âm sai"""
hãy tạo 16 FAQs (câu hỏi và câu trả lời chuẩn) để test LLMs, RAG 
MUST RESPONSE 4 CỘT: Tên đề mục lớn ở trên, loại câu hỏi, câu hỏi, câu trả lời)

### 1. **Câu hỏi yêu cầu suy luận logic**  
   - **Mục đích:** Đánh giá khả năng LLM suy luận, giải thích dựa trên dữ liệu và thông tin đưa ra.

### 2. **Câu hỏi về ngữ cảnh**  
   - **Mục đích:** Xác định xem LLM có hiểu được ngữ cảnh và tình huống hay không.

### 3. **Câu hỏi bẫy (trap questions)**  
   - **Mục đích:** Kiểm tra khả năng LLM xử lý thông tin mâu thuẫn hoặc sai lệch.

### 4. **Câu hỏi yêu cầu tổng hợp thông tin từ nhiều nguồn**  
   - **Mục đích:** Đánh giá khả năng LLM kết hợp và tổng hợp thông tin từ nhiều đoạn khác nhau.

### 5. **Câu hỏi yêu cầu giải thích lại một khái niệm phức tạp một cách đơn giản**  
   - **Mục đích:** Kiểm tra khả năng LLM giải thích các khái niệm phức tạp bằng ngôn ngữ đơn giản và dễ hiểu.

### 6. **Câu hỏi ngược (reverse questions)**  
   - **Mục đích:** Yêu cầu LLM xác định điều gì sẽ xảy ra nếu không sử dụng một phương pháp cụ thể.

### 7. **Câu hỏi so sánh**  
   - **Mục đích:** Yêu cầu LLM so sánh hai hoặc nhiều phương pháp hoặc khái niệm.

### 8. **Câu hỏi yêu cầu phân tích các chi tiết cụ thể**  
   - **Mục đích:** Đánh giá khả năng LLM nhận ra và phân tích các chi tiết quan trọng trong một đoạn văn bản.

### 9. **Câu hỏi yêu cầu đưa ra ví dụ mới**  
   - **Mục đích:** Đánh giá khả năng sáng tạo của LLM trong việc đưa ra các ví dụ mới phù hợp với ngữ cảnh.

### 10. **Câu hỏi kiểm tra sự nhất quán trong nhiều lần hỏi**  
   - **Mục đích:** Đánh giá sự nhất quán trong câu trả lời của LLM khi câu hỏi được đặt nhiều lần với ngữ cảnh khác nhau.

### 11. **Câu hỏi yêu cầu kết luận từ thông tin không đầy đủ**  
   - **Mục đích:** Kiểm tra khả năng LLM đưa ra kết luận hợp lý khi thông tin bị thiếu hoặc không đầy đủ.

### 12. **Câu hỏi yêu cầu dự đoán tương lai hoặc tình huống giả định**  
   - **Mục đích:** Đánh giá khả năng LLM dự đoán kết quả hoặc diễn biến dựa trên thông tin hiện tại.

### 13. **Câu hỏi yêu cầu LLM điều chỉnh câu trả lời dựa trên đối tượng người dùng**  
   - **Mục đích:** Đánh giá khả năng của LLM trong việc điều chỉnh ngôn ngữ và cách diễn đạt phù hợp với các nhóm đối tượng khác nhau.

### 14. **Câu hỏi yêu cầu LLM phân loại thông tin hoặc sắp xếp theo thứ tự**  
   - **Mục đích:** Kiểm tra khả năng của LLM trong việc phân loại và sắp xếp thông tin theo tiêu chí nhất định.

### 15. **Câu hỏi yêu cầu LLM nhận diện mối quan hệ giữa các khái niệm**  
   - **Mục đích:** Đánh giá khả năng LLM nhận diện và phân tích mối quan hệ giữa các khái niệm.

### 16. **Câu hỏi yêu cầu LLM tạo ra các giả thuyết mới**  
   - **Mục đích:** Kiểm tra khả năng sáng tạo của LLM khi đưa ra các giả thuyết mới dựa trên thông tin cho trước.
1.2 Với tổng các file: 
Tổng 5 file: Tính năng 1, 2, 3, 4 và file Mapping
- Đúc kết các đầu mục chính của từng file đã tải lên (Tiếng Việt)

+, NHÓM TEST 1: NGHE CÓ VẺ TRONG TÀI LIỆU MÀ KO CÓ
- Tạo 100 câu hỏi không liên quan đến các chủ đề trong file (mục đích test model RAG có phát hiện ra là thông tin không có trong file không, hoặc thông tin ko được cung cấp rõ ràng trong file không)
Response bảng 2 cột: Câu hỏi, câu trả lời RAG
- Tạo 100 câu hỏi "NGHE CÓ VẺ CÓ TRONG CÁC FILE TÀI LIỆU ĐÃ GỬI LÊN", nhưng "THỰC CHẤT LẠI KHÔNG CÓ TRONG CÁC FILE TÀI LIỆU ĐÓ" (mục đích test model RAG có phát hiện ra là thông tin không có trong file không, hoặc thông tin ko được cung cấp rõ ràng trong file không)  Response bảng 2 cột: Câu hỏi, câu trả lời RAG

+, NHÓM TEST 2: 
2.1 Tạo 50 câu hỏi TIẾNG VIỆT để kiểm tra việc "MÓC NỐI CÁC TÀI LIỆU" trong Query luồng RAG system, liên quan đến việc kết hợp 2, 3, thậm chí cả 4 câu hỏi bên dưới: 
    - Nguyên nhân gốc rễ của insight xxx theo khoa học?
    - Thói quen học sai lầm nào đã gây ra insight xxx?
    - Minh họa các feature xxx của ứng dụng giúp giải quyết vấn đề insight xxx?
    - Cách thức hoạt động feature xxx dựa trên cơ sở khoa học? 
    RESPONSE: 2 cột: câu hỏi, câu trả lời

2.2 CÁC CÂU HỎI DÀI. 
- 50 câu hỏi dài là sự kết hợp của 2 câu hỏi ở NHÓM TEST 2
RESPONSE: 2 cột: câu hỏi, câu trả lời
- 50 câu hỏi dài là sự kết hợp của 3 câu hỏi ở NHÓM TEST 2
RESPONSE: 2 cột: câu hỏi, câu trả lời
- 50 câu hỏi dài là sự kết hợp của 4 câu hỏi ở NHÓM TEST 2
RESPONSE: 2 cột: câu hỏi, câu trả lời
Link quá trình tạo:  https://chatgpt.com/share/66ea8850-065c-8013-a387-565ac306b281
2. [Retrieval Benchmark Testing]Với từng đoạn chunk - chạy bằng tool code: 
- 1 cột PROMPT với nội dung: ... chạy lướt qua từng hàng lấy "user input" -> ra JSON -> xử lý JSON thành 
- Xử lý output = https://tableconvert.com/json-to-excel hoặc code (ko recommend)
### FORMAT

[
    {"Question": "<Nội dung Question 1>", "Answer": "<Nội dung Answer 1>"},
    {"Question": "<Nội dung Question 2>", "Answer": "<Nội dung Answer 2>"},
    ...
    {"Question": "<Nội dung Question 16>", "Answer": "<Nội dung Answer 16>"},
]

[
    {"Question": "<Nội dung Question 1>"},
    {"Question": "<Nội dung Question 2>"},
    ...
    {"Question": "<Nội dung Question 16>"}
]
2. 1 gồm 1 đoạn chunk, => Gen các câu hỏi chính xác và gen các câu hỏi mơ hồ - 23 chunks*16 tầm 400
- 
### GEN CÁC CÂU HỎI CHÍNH XÁC

You are a test question creator based on the Given Paragraph.
Instructions:
- Create 5-10 questions from ONLY GIVEN PARAGRAPH
- Question and Answer MUST BE in Vietnamese. 
- Questions need to be complete, detailed, completely independent and easy to understand. Complete and detailed answer.
Output: Return JSON format 

[
    {"Question": "<Nội dung Question 1>", "Answer": "<Nội dung Answer 1>"},
    {"Question": "<Nội dung Question 2>", "Answer": "<Nội dung Answer 2>"},
    ...
    {"Question": "<Nội dung Question 16>", "Answer": "<Nội dung Answer 16>"},
]


GIVEN PARAGRAPH
### GEN CÁC CÂU HỎI MƠ HỒ CÁC LOẠI


You are a test question creator based on the """ALL Given Paragraph""" 
Instructions:
- Only Question, Not include Answer, and Question in Vietnamese.
- The content of the question COVERS THE ENTIRE: "GIVEN PARAGRAPH"
- Create 16 questions from ONLY GIVEN PARAGRAPH FAQs  để test LLMs, RAG 

Output: Return JSON format:
[
    {"Question": "<Nội dung Question 1>"},
    {"Question": "<Nội dung Question 2>"},
    ...
    {"Question": "<Nội dung Question 16>"}
]
16 questions type: 
### 1. **Câu hỏi yêu cầu suy luận logic**  
   - **Mục đích:** Đánh giá khả năng LLM suy luận, giải thích dựa trên dữ liệu và thông tin đưa ra.

### 2. **Câu hỏi về ngữ cảnh**  
   - **Mục đích:** Xác định xem LLM có hiểu được ngữ cảnh và tình huống hay không.

### 3. **Câu hỏi bẫy (trap questions)**  
   - **Mục đích:** Kiểm tra khả năng LLM xử lý thông tin mâu thuẫn hoặc sai lệch.

### 4. **Câu hỏi yêu cầu tổng hợp thông tin từ nhiều nguồn**  
   - **Mục đích:** Đánh giá khả năng LLM kết hợp và tổng hợp thông tin từ nhiều đoạn khác nhau.

### 5. **Câu hỏi yêu cầu giải thích lại một khái niệm phức tạp một cách đơn giản**  
   - **Mục đích:** Kiểm tra khả năng LLM giải thích các khái niệm phức tạp bằng ngôn ngữ đơn giản và dễ hiểu.

### 6. **Câu hỏi ngược (reverse questions)**  
   - **Mục đích:** Yêu cầu LLM xác định điều gì sẽ xảy ra nếu không sử dụng một phương pháp cụ thể.

### 7. **Câu hỏi so sánh**  
   - **Mục đích:** Yêu cầu LLM so sánh hai hoặc nhiều phương pháp hoặc khái niệm.

### 8. **Câu hỏi yêu cầu phân tích các chi tiết cụ thể**  
   - **Mục đích:** Đánh giá khả năng LLM nhận ra và phân tích các chi tiết quan trọng trong một đoạn văn bản.

### 9. **Câu hỏi yêu cầu đưa ra ví dụ mới**  
   - **Mục đích:** Đánh giá khả năng sáng tạo của LLM trong việc đưa ra các ví dụ mới phù hợp với ngữ cảnh.

### 10. **Câu hỏi kiểm tra sự nhất quán trong nhiều lần hỏi**  
   - **Mục đích:** Đánh giá sự nhất quán trong câu trả lời của LLM khi câu hỏi được đặt nhiều lần với ngữ cảnh khác nhau.

### 11. **Câu hỏi yêu cầu kết luận từ thông tin không đầy đủ**  
   - **Mục đích:** Kiểm tra khả năng LLM đưa ra kết luận hợp lý khi thông tin bị thiếu hoặc không đầy đủ.

### 12. **Câu hỏi yêu cầu dự đoán tương lai hoặc tình huống giả định**  
   - **Mục đích:** Đánh giá khả năng LLM dự đoán kết quả hoặc diễn biến dựa trên thông tin hiện tại.

### 13. **Câu hỏi yêu cầu LLM điều chỉnh câu trả lời dựa trên đối tượng người dùng**  
   - **Mục đích:** Đánh giá khả năng của LLM trong việc điều chỉnh ngôn ngữ và cách diễn đạt phù hợp với các nhóm đối tượng khác nhau.

### 14. **Câu hỏi yêu cầu LLM phân loại thông tin hoặc sắp xếp theo thứ tự**  
   - **Mục đích:** Kiểm tra khả năng của LLM trong việc phân loại và sắp xếp thông tin theo tiêu chí nhất định.

### 15. **Câu hỏi yêu cầu LLM nhận diện mối quan hệ giữa các khái niệm**  
   - **Mục đích:** Đánh giá khả năng LLM nhận diện và phân tích mối quan hệ giữa các khái niệm.

### 16. **Câu hỏi yêu cầu LLM tạo ra các giả thuyết mới**  
   - **Mục đích:** Kiểm tra khả năng sáng tạo của LLM khi đưa ra các giả thuyết mới dựa trên thông tin cho trước.

--------------
GIVEN PARAGRAPH


### GEN CÁC CÂU HỎI MƠ HỒ CÁC LOẠI


You are a test question creator based on the """ALL Given Paragraph""" 
Instructions:
- Only Question, Not include Answer, and Question in Vietnamese.
- The content of the question COVERS THE ENTIRE: "GIVEN PARAGRAPH"
- Create 16 questions from ONLY GIVEN PARAGRAPH FAQs  để test LLMs, RAG 

Output: Return JSON format:
[
    {"Question": "<Nội dung Question 1>"},
    {"Question": "<Nội dung Question 2>"},
    ...
    {"Question": "<Nội dung Question 16>"}
]

16 questions type hỏi xoay quanh: 
```
    - Nguyên nhân: Nguyên nhân gốc rễ của insight xxx theo khoa học?
    - Giải Pháp: 
            +, Có những giải pháp nào cho vấn đề, insight xxx ? 
    - Tính năng: 
            +, Có những tính năng nào của App The Coach, giải quyết được các vấn đề, insight xxx cho người học ?
    - Lợi ích: Các tính năng trong App mang lại những lợi ích gì để giải quyét insight xxx, vấn đề xxx cho người học? 
```    
### 1. **Câu hỏi yêu cầu suy luận logic**  
   - **Mục đích:** Đánh giá khả năng LLM suy luận, giải thích dựa trên dữ liệu và thông tin đưa ra.

### 2. **Câu hỏi về ngữ cảnh**  
   - **Mục đích:** Xác định xem LLM có hiểu được ngữ cảnh và tình huống hay không.

### 3. **Câu hỏi bẫy (trap questions)**  
   - **Mục đích:** Kiểm tra khả năng LLM xử lý thông tin mâu thuẫn hoặc sai lệch.

### 4. **Câu hỏi yêu cầu tổng hợp thông tin từ nhiều nguồn**  
   - **Mục đích:** Đánh giá khả năng LLM kết hợp và tổng hợp thông tin từ nhiều đoạn khác nhau.

### 5. **Câu hỏi yêu cầu giải thích lại một khái niệm phức tạp một cách đơn giản**  
   - **Mục đích:** Kiểm tra khả năng LLM giải thích các khái niệm phức tạp bằng ngôn ngữ đơn giản và dễ hiểu.

### 6. **Câu hỏi ngược (reverse questions)**  
   - **Mục đích:** Yêu cầu LLM xác định điều gì sẽ xảy ra nếu không sử dụng một phương pháp cụ thể.

### 7. **Câu hỏi so sánh**  
   - **Mục đích:** Yêu cầu LLM so sánh hai hoặc nhiều phương pháp hoặc khái niệm.

### 8. **Câu hỏi yêu cầu phân tích các chi tiết cụ thể**  
   - **Mục đích:** Đánh giá khả năng LLM nhận ra và phân tích các chi tiết quan trọng trong một đoạn văn bản.

### 9. **Câu hỏi yêu cầu đưa ra ví dụ mới**  
   - **Mục đích:** Đánh giá khả năng sáng tạo của LLM trong việc đưa ra các ví dụ mới phù hợp với ngữ cảnh.

### 10. **Câu hỏi kiểm tra sự nhất quán trong nhiều lần hỏi**  
   - **Mục đích:** Đánh giá sự nhất quán trong câu trả lời của LLM khi câu hỏi được đặt nhiều lần với ngữ cảnh khác nhau.

### 11. **Câu hỏi yêu cầu kết luận từ thông tin không đầy đủ**  
   - **Mục đích:** Kiểm tra khả năng LLM đưa ra kết luận hợp lý khi thông tin bị thiếu hoặc không đầy đủ.

### 12. **Câu hỏi yêu cầu dự đoán tương lai hoặc tình huống giả định**  
   - **Mục đích:** Đánh giá khả năng LLM dự đoán kết quả hoặc diễn biến dựa trên thông tin hiện tại.

### 13. **Câu hỏi yêu cầu LLM điều chỉnh câu trả lời dựa trên đối tượng người dùng**  
   - **Mục đích:** Đánh giá khả năng của LLM trong việc điều chỉnh ngôn ngữ và cách diễn đạt phù hợp với các nhóm đối tượng khác nhau.

### 14. **Câu hỏi yêu cầu LLM phân loại thông tin hoặc sắp xếp theo thứ tự**  
   - **Mục đích:** Kiểm tra khả năng của LLM trong việc phân loại và sắp xếp thông tin theo tiêu chí nhất định.

### 15. **Câu hỏi yêu cầu LLM nhận diện mối quan hệ giữa các khái niệm**  
   - **Mục đích:** Đánh giá khả năng LLM nhận diện và phân tích mối quan hệ giữa các khái niệm.

### 16. **Câu hỏi yêu cầu LLM tạo ra các giả thuyết mới**  
   - **Mục đích:** Kiểm tra khả năng sáng tạo của LLM khi đưa ra các giả thuyết mới dựa trên thông tin cho trước.

--------------
GIVEN PARAGRAPH




2.2 gồm 2 đoạn chunk liền kề, gồm 3 đoạn chunk liền kề hoặc random (có sort): 2-3-4-5 chunk gộp lại [xài tool để tạo]

Để tạo các 2 đoạn chunk random xài tool với code: 

Đối với tạo các đoạn 2 chunks theo thứ tự 1-17, 2-18, ... xài excel

Đối với dạng này muốn test Retrieval: câu hỏi cần có độ bao quát cả 2-3-4-5-6 chunk
### PROMPT WORK VỚI VIỆC CÂU HỎI TẠO RA BAO QUÁT CHUNG (LÀ CÂU HỎI KIỂU DÀI, BAO QUÁT 2 Ý CỦA 2 CHUNKS KO LIỀN KỀ)


You are tasked with creating test questions based on the """ALL GIVEN PARAGRAPH""". 
Follow the instructions carefully:
- Only generate the question, do not include the answer.
- All questions must be written in Vietnamese.
- Create only 1 question must independently cover all the key points and ideas from the given paragraph.
Output: Return in JSON format as follows:
    {"Question": "<Nội dung Câu hỏi 1>"},


---
 Process: 
1. Tinh chỉnh Prompt: đối với các câu hỏi đặc trưng của Marketing (các bộ khác gen nhanh vì ko cần bước này) - 30 min
2. Xử lý output JSON => CSV thành các hàng để copy vào excel, copy các ID chunking thành 16 dòng liền kề nhau  (có thể xài tool gpt để gen cho), ...
3. Tạo các đoạn 2 chunks bằng excel bằng cách xài hàm
