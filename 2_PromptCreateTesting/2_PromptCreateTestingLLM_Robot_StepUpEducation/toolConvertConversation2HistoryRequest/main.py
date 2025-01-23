# ```
# 1. Input: 

# ```bash
# Role	Content
# roleA	sẵn sàng
# roleB	Chào cậu! Hôm nay chúng ta sẽ học về chủ đề đồ ăn nhé! Các món ăn yêu thích của cậu là gì nào?
# roleA	Tớ thích phở, bánh mì. Tớ cũng thích kem.
# roleB	Thật tuyệt! Cậu thích phở, bánh mì và kem. Hôm nay tớ sẽ giúp cậu nói về các món ăn này nhé! Đầu tiên, cậu hãy nói "Pho" cho tớ nào!
# roleA	Tớ nói "Phở".
# roleB	Tuyệt vời! Cậu đã nói đúng rồi! Giờ chúng ta cùng nói về món "Bánh mì" nhé! Cậu hãy thử nói "Banh mi" nào!
# ```


# 2. Output: 

# ```
# conversation_history	previous_assistant_response	user_answer	next_assistant_response
			
# 		sẵn sàng	Chào cậu! Hôm nay chúng ta sẽ học về chủ đề đồ ăn nhé! Các món ăn yêu thích của cậu là gì nào?
			
# "[
#         {
#                 ""role"": ""user"",
#                 ""content"": ""sẵn sàng""
#         },
#         {
#                 ""role"": ""assistant"",
#                 ""content"": ""Chào em! Hôm nay chúng ta sẽ học cách mở rộng một câu nói để diễn đạt ý đầy đủ hơn. Em sẵn sàng chưa?""
#         }
# ]"	Chào cậu! Hôm nay chúng ta sẽ học về chủ đề đồ ăn nhé! Các món ăn yêu thích của cậu là gì nào?	Tớ thích phở, bánh mì. Tớ cũng thích kem.	Thật tuyệt! Cậu thích phở, bánh mì và kem. Hôm nay tớ sẽ giúp cậu nói về các món ăn này nhé! Đầu tiên, cậu hãy nói "Pho" cho tớ nào!
			
# "[
#         {
#                 ""role"": ""user"",
#                 ""content"": ""sẵn sàng""
#         },
#         {
#                 ""role"": ""assistant"",
#                 ""content"": ""Chào em! Hôm nay chúng ta sẽ học cách mở rộng một câu nói để diễn đạt ý đầy đủ hơn. Em sẵn sàng chưa?""
#         }, 
#         {
#                 ""role"": ""user"",
#                 ""content"": ""Tớ thích phở, bánh mì. Tớ cũng thích kem.""
#         },
#         {
#                 ""role"": ""assistant"",
#                 ""content"": ""Thật tuyệt! Cậu thích phở, bánh mì và kem. Hôm nay tớ sẽ giúp cậu nói về các món ăn này nhé! Đầu tiên, cậu hãy nói ""Pho"" cho tớ nào!""
#         }
# ]"	Thật tuyệt! Cậu thích phở, bánh mì và kem. Hôm nay tớ sẽ giúp cậu nói về các món ăn này nhé! Đầu tiên, cậu hãy nói "Pho" cho tớ nào!	Tớ nói "Phở".	Tuyệt vời! Cậu đã nói đúng rồi! Giờ chúng ta cùng nói về món "Bánh mì" nhé! Cậu hãy thử nói "Banh mi" nào!
# ```
# ```

# ----
# Code đi 