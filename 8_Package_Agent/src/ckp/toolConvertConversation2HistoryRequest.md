1. Input: 

```bash
Role	Content
roleA	sẵn sàng
roleB	Chào cậu! Hôm nay chúng ta sẽ học về chủ đề đồ ăn nhé! Các món ăn yêu thích của cậu là gì nào?
roleA	Tớ thích phở, bánh mì. Tớ cũng thích kem.
roleB	Thật tuyệt! Cậu thích phở, bánh mì và kem. Hôm nay tớ sẽ giúp cậu nói về các món ăn này nhé! Đầu tiên, cậu hãy nói "Pho" cho tớ nào!
roleA	Tớ nói "Phở".
roleB	Tuyệt vời! Cậu đã nói đúng rồi! Giờ chúng ta cùng nói về món "Bánh mì" nhé! Cậu hãy thử nói "Banh mi" nào!
```


2. Output: 

```
conversation_history	previous_assistant_response	user_answer	next_assistant_response
			
		sẵn sàng	Chào cậu! Hôm nay chúng ta sẽ học về chủ đề đồ ăn nhé! Các món ăn yêu thích của cậu là gì nào?
			
"[
        {
                ""role"": ""user"",
                ""content"": ""sẵn sàng""
        },
        {
                ""role"": ""assistant"",
                ""content"": ""Chào em! Hôm nay chúng ta sẽ học cách mở rộng một câu nói để diễn đạt ý đầy đủ hơn. Em sẵn sàng chưa?""
        }
]"	Chào cậu! Hôm nay chúng ta sẽ học về chủ đề đồ ăn nhé! Các món ăn yêu thích của cậu là gì nào?	Tớ thích phở, bánh mì. Tớ cũng thích kem.	Thật tuyệt! Cậu thích phở, bánh mì và kem. Hôm nay tớ sẽ giúp cậu nói về các món ăn này nhé! Đầu tiên, cậu hãy nói "Pho" cho tớ nào!
			
"[
        {
                ""role"": ""user"",
                ""content"": ""sẵn sàng""
        },
        {
                ""role"": ""assistant"",
                ""content"": ""Chào em! Hôm nay chúng ta sẽ học cách mở rộng một câu nói để diễn đạt ý đầy đủ hơn. Em sẵn sàng chưa?""
        }, 
        {
                ""role"": ""user"",
                ""content"": ""Tớ thích phở, bánh mì. Tớ cũng thích kem.""
        },
        {
                ""role"": ""assistant"",
                ""content"": ""Thật tuyệt! Cậu thích phở, bánh mì và kem. Hôm nay tớ sẽ giúp cậu nói về các món ăn này nhé! Đầu tiên, cậu hãy nói ""Pho"" cho tớ nào!""
        }
]"	Thật tuyệt! Cậu thích phở, bánh mì và kem. Hôm nay tớ sẽ giúp cậu nói về các món ăn này nhé! Đầu tiên, cậu hãy nói "Pho" cho tớ nào!	Tớ nói "Phở".	Tuyệt vời! Cậu đã nói đúng rồi! Giờ chúng ta cùng nói về món "Bánh mì" nhé! Cậu hãy thử nói "Banh mi" nào!
```




INSTRUCTION: 
```bash
B1. Các dòng ở file input được sắp xếp lần lượt là: role A - role B - role A - role B 
B2. Output có 4 cột: conversation_history, previous_assistant_response, user_answer, next_assistant_response
B3. Tại mỗi dòng role='roleA', page nội dung ở cột 'Role' vào user_answer (2 cột previous và next assistant response thì nhớ lấy trước và sau). 
B4. Update previous_conversation_history
-------
```