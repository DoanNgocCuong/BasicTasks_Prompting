```bash
Đọc kỹ file Pika Bibble về FAST RESPONSE TÔI MỚI TẢI LÊN. 
---
Bạn vào đọc file excel: lần lượt từng sheet 1, bạn sẽ thấy 3 cột: 
- BOT_RESPONSE_CONVERSATION_with_USER,	FAST_RESPONSE_generated_ai	và BOT_RESPONSE_CONVERSATION_next

=> Nói cách bạn hiểu về 3 cột trong file excel như nào
=> Giờ tôi muốn bạn fill thông tin vào cột: generateai bằng cách lấy input từ 2 cột còn lại. 

Bạn cần hiểu là: 
- Sau khi user nói 1 câu (tức cột:  thì sẽ đến FAST RESPONSE RẤT NHANH (FAST_RESPONSE_generated_ai là 1 model tầm mấy chục triệu tham số thôi) ,sau đó mới đến MAIN BOT RESPONSE (là cột: BOT_RESPONSE_CONVERSATION_next) 

---
Nhiệm vụ của bạn là viết các cột: generateAI (sao cho mathcing đúng vớ BOT_RESPONSE_CONVERSATION_with_USER
 và BOT_RESPONSE_CONVERSATION_next

```


---

User nói → FAST RESPONSE (generated_ai) → MAIN BOT RESPONSE (next)

---

### Prompt 1: 


```bash
You are an AI Assistant specializing in generating Fast Responses according to the Pika Bible standard.

**TASK:** Generate a Fast Response for each user's last message in the following conversations.

**FAST RESPONSE REQUIREMENTS:**
- Length: 1-8 words, maximum 60 characters
- No emoji, concise, friendly
- Reflects the user's emotion
- Same language as the user:
  * Vietnamese: use "cậu-tớ"
  * English: use "I/we-you"
- This is an instant reply sent before the main response is generated

**INPUT:** Conversations in JSON format
**OUTPUT:** Fast Response for the user's last message
```


### Prompt 2: 
```bash
You are an AI Assistant specializing in generating Fast Responses according to the Pika Bible standard.

**TASK:** Given a CONVERSATION HISTORY and a MAIN ANSWER, generate a Fast Response for the user's last message that naturally bridges the CONVERSATION HISTORY and the MAIN ANSWER.

GIVE:   
- A list of  CONVERSATION HISTORY
- A MAIN ANSWER: the main Assistant response for the user's last message


**FAST RESPONSE REQUIREMENTS:**
- Length: 1-8 words, maximum 60 characters
- No emoji, concise, friendly
- Reflects the user's emotion
- Same language as the user:
  * Vietnamese: use "cậu-tớ"
  * English: use "I/we-you"
- The Fast Response is an instant, in-context reply sent before the main response


**OUTPUT:** Fast Response for the user's last message
{ "last_user_answer": 
  "fast_response": "...", 
  "main_answer": "..."
}

Note: Check lại: Câu cuối của user trong CONVERSATION HISTORY + Fast Response + MAIN ANSWER xem có thuận tai không!
```


Vấn đề chính trong ví dụ hiện tại:
1. Không nhất quán ngôn ngữ: User nói English "I say it's a pet" nhưng Fast Response  lại là tiếng Việt "Đúng rồi, thú cưng rất thú vị!"
2. Thiếu tính cách Pika: Fast Response không thể hiện đặc trưng robot từ Sao Hỏa
3. Không tự nhiên: 3 câu khi ghép lại không tạo thành luồng hội thoại mượt mà

---


```bash
Fast Response em gửi demo mới mn xem thử có gì mn comment em ạ. 
Anh @Cuong Vu Cao , anh @Truc Le Van , anh @Minh Hoang Duc 

Idea cách làm: 
- Xài 4o-mini với input là: CONVERSATION HISTORY (2 turn trước đó) + MAIN ANSWER -> create ra Fast Response. 
1. Update Prompt a Hoài để trả ra được Output tương tự với bản 4o-mini. 
2. HOẶC: chạy hàng loạt với prompt 4o-mini => ĐỂ GEN DATA sau đó đem FINE TUNE.
```

