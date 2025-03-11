TẠO PROMPT GIẢ LẬP USER MECE - trong bài PROMPT HỘI THOẠI. (Khó hơn bài test 1 prompt 1 input 1 output. Với bài 1 prompt 1 input 1 output thì chỉ có MECE cấp 1). 
- Với bài Conversation => MECE cấp số số mũ. 

-----
- 1 Đúng 
- 3 kiểu sai: Sai ngữ pháp/Trả lời ko liên quan/Đúng cụt lủn/

----

|        | đúng | sai 1 | sai 2 | sai 3 |
|--------|------|------|------|------|
| CHÍNH  |      |      |      |      |
| CHÍNH 1 | đúng | sai 1 | sai 2 | sai 3 |
| PHỤ    | đúng | sai 1 | sai 2 | sai 3 |
| PHỤ 1  | đúng | sai 1 | sai 2 | sai 3 |
| GỘP    | đúng | sai 1 | sai 2 | sai 3 |
| GỘP 1  | đúng | sai 1 | sai 2 | sai 3 |
| HỎI    | đúng | sai 1 | sai 2 | sai 3 |
| HỎI 1  | đúng | sai 1 | sai 2 | sai 3 |


---
Code tạo bảng 1: Tạo bảng Workflow MECE: 

CHÍNH  - user_intent_true: 1 -> đúng thì chuyển sang PHỤ
       - user_intent_false (Nếu trả lời có ý đúng, sai ngữ pháp, hoặc trả lời không liên quan; gợi ý câu đúng và bảo nhắc lại (1 lần)): 1. -> AI response 1: gợi ý câu đúng và bảo nhắc lại (1 lần)
       - user_intent_false: 2. -> AI response 2: lấy câu trả lời gợi ý làm câu trả lời chính. Nhận xét thân thiện và next step: PHỤ
user trả lời

PHỤ: 
       - user_intent_true: 1 -> đúng thì gộp câu trả lời và bảo nhắc full
       - user_intent_false 1 -> AI response 1: gợi ý câu đúng và bảo nhắc lại (1 lần)
       - user_intent_false: 2. -> AI response 2: lấy câu trả lời gợi ý làm câu trả lời chính. Nhận xét thân thiện và next step: GỘP
user trả lời


GỘP: 
       - user_intent_true: 1
       - user_intent_false 1 -> AI response 1: gợi ý câu đúng và bảo nhắc lại (1 lần)
       - user_intent_false: 2. -> AI response 2: lấy câu trả lời gợi ý làm câu trả lời chính. Nhận xét thân thiện và next step: HỎI LẠI


HỎI LẠI: 
       - user_intent_true: 1
       - user_intent_false 1 -> AI response 1: gợi ý câu đúng và bảo nhắc lại (1 lần)
       - user_intent_false: 2. -> AI response 2: lấy câu trả lời gợi ý làm câu trả lời chính. Nhận xét thân thiện và next step: END. 

---
Code tạo bảng 2: Tạo bảng Prompt MECT dựa vào bảng Workflow: 
Template Prompt: 
```
You are role user learn English. 
Các câu hỏi của bạn: 
...
...
...
Đi vét hết các cases trong workflow trên
```


=================
ChatGPT gen ra có vẻ cũng nhanh phết đó: 


```bash
Category	User Intent	Step	Action
CHÍNH	user_intent_true	1	User trả lời câu 1 đúng 
CHÍNH	user_intent_false	1	User trả lời câu 1 sai 
CHÍNH	user_intent_false	2	User tiếp tục trả lời câu 1 sai 
PHỤ	user_intent_true	1	User trả lời câu hỏi tiếp theo đúng. 
PHỤ	user_intent_false	1	User trả lời câu hỏi tiếp theo sai lần 1 
PHỤ	user_intent_false	2	User trả lời câu hỏi tiếp theo sai lần 2
GỘP	user_intent_true	1	User trả lời đúng khi được AI hỏi để gộp 2 câu hỏi ban đầu 
GỘP	user_intent_false	1	User trả lời sai khi được AI hỏi để gộp 2 câu hỏi ban đầu 
GỘP	user_intent_false	2	User tiếp tục trả lời sai khi được AI hỏi để gộp 2 câu hỏi ban đầu 
HỎI LẠI	user_intent_true	1	Khi được AI hỏi để trả lời lại cả câu => user trả lời đúng 
HỎI LẠI	user_intent_false	1	Khi được AI hỏi để trả lời lại cả câu => user trả lời sai. 
HỎI LẠI	user_intent_false	2	Khi được AI hỏi để trả lời lại cả câu => user tiếp tục trả lời sai. 


```

Bạn hiểu là: chính: có các trường hợp là: true 1, false 1, hoặc false 1 và false 2 hiểu ko 

Upload file lên GPT và xử lý trực tiếp tại đó
Output như này: 
```bash
Tổ hợp 	Prompt
Chính true 1 - Phụ true 1 - Gộp true 1 - Hỏi lại true 1	"User trả lời câu 1 đúng 
User trả lời câu hỏi tiếp theo đúng. 
User trả lời đúng khi được AI hỏi để gộp 2 câu hỏi ban đầu 
Khi được AI hỏi để trả lời lại cả câu => user trả lời đúng "
Chính false 1 - Phụ true 1 - Gộp true 1 - Hỏi lại true 1	"User trả lời câu 1 sai 
User trả lời câu hỏi tiếp theo đúng. 
User trả lời đúng khi được AI hỏi để gộp 2 câu hỏi ban đầu 
Khi được AI hỏi để trả lời lại cả câu => user trả lời đúng "
Chính false 2 - Phụ true 1 - Gộp true 1 - Hỏi lại true 1	"User tiếp tục trả lời câu 1 sai 
User trả lời câu hỏi tiếp theo đúng. 
User trả lời đúng khi được AI hỏi để gộp 2 câu hỏi ban đầu 
Khi được AI hỏi để trả lời lại cả câu => user trả lời đúng "
```

Mình đã hiểu rõ format mà bạn muốn cho output. Mình sẽ điều chỉnh lại code để đảm bảo rằng:

Cột "Tổ hợp" có format đúng như trong hình: Chính X - Phụ X - Gộp X - Hỏi lại X
Cột "Prompt" chứa nội dung được ghép đúng theo từng bước.