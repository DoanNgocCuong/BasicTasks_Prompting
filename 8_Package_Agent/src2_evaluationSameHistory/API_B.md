```
curl --location 'http://103.253.20.13:9400/personalized-ai-coach/api/v1/bot/initConversation' \
--header 'Content-Type: application/json' \
--data '{
    "bot_id": 47,
    "conversation_id": "123456",
    "input_slots": {}
}'
```

```
curl --location 'http://103.253.20.13:9400/personalized-ai-coach/api/v1/bot/webhook' \
--header 'Content-Type: application/json' \
--data '{
    "conversation_id": "123456",
    "message": "Tớ thích phở sáng. Bữa sáng ngon!",
    "history": [
        {
            "role": "user",
            "content": "sẵn sàng"
        }, 
        {
            "role": "assistant",
            "content": "Hello! Xin chào! Tớ là Pika. Hôm nay, chúng ta có thể nói về bất cứ chủ đề nào mà cậu thích như đồ ăn, động vật, trò chơi, bạn bè. What do you want to talk about?"
        }, 
        {
            "role": "user",
            "content": "Tớ thích đồ ăn. Món nào ngon?"
        }, 
        {
            "role": "assistant",
            "content": "Food is delicious and there are many types to try. Đồ ăn Việt Nam có nhiều món ngon như phở, bánh mì, và gỏi cuốn, cậu có món yêu thích không?"
        }, 
        {
            "role": "user",
            "content": "Tớ thích phở. Ngon quá đi!"
        }, 
        {
            "role": "assistant",
            "content": "Phở is a popular Vietnamese dish made with beef or chicken broth and noodles. Phở thường được ăn với rau thơm và chanh, làm cho món ăn trở nên tươi ngon hơn, cậu thích ăn phở vào buổi sáng hay buổi tối?"
        }
    ],
    "question_idx": 1
}'
```

Luồng Agent, Call History


```
File exel: 

conversation_history	user_answer
	
"[
    
]"	sẵn sàng
"[
    {""role"": ""roleA"", ""content"": ""sẵn sàng""},
    {""role"": ""roleB"", ""content"": ""Hello! Xin chào! Tớ là Pika. Hôm nay, chúng ta có thể nói về bất cứ chủ đề nào mà cậu thích như đồ ăn, động vật, trò chơi, bạn bè. What do you want to talk about?""}
]"	Tớ thích động vật. Cậu thích gì?
"[
    {""role"": ""roleA"", ""content"": ""sẵn sàng""},
    {""role"": ""roleB"", ""content"": ""Hello! Xin chào! Tớ là Pika. Hôm nay, chúng ta có thể nói về bất cứ chủ đề nào mà cậu thích như đồ ăn, động vật, trò chơi, bạn bè. What do you want to talk about?""},
    {""role"": ""roleA"", ""content"": ""Tớ thích động vật. Cậu thích gì?""},
    {""role"": ""roleB"", ""content"": ""I like learning about different kinds of animals. Động vật có rất nhiều loài thú vị và độc đáo, như loài mèo có thể nhảy cao và loài chó có thể chạy nhanh. What is your favorite animal?""}
]"	Tớ thích mèo. Mèo dễ thương!
"[
    {""role"": ""roleA"", ""content"": ""sẵn sàng""},
    {""role"": ""roleB"", ""content"": ""Hello! Xin chào! Tớ là Pika. Hôm nay, chúng ta có thể nói về bất cứ chủ đề nào mà cậu thích như đồ ăn, động vật, trò chơi, bạn bè. What do you want to talk about?""},
    {""role"": ""roleA"", ""content"": ""Tớ thích động vật. Cậu thích gì?""},
    {""role"": ""roleB"", ""content"": ""I like learning about different kinds of animals. Động vật có rất nhiều loài thú vị và độc đáo, như loài mèo có thể nhảy cao và loài chó có thể chạy nhanh. What is your favorite animal?""},
    {""role"": ""roleA"", ""content"": ""Tớ thích mèo. Mèo dễ thương!""},
    {""role"": ""roleB"", ""content"": ""Cats are very cute and can be great pets. Mèo có thể ngủ 12-16 tiếng mỗi ngày và chúng có khả năng phát ra hơn 100 âm thanh khác nhau để giao tiếp. What do you like most about cats?""}
]"	Tớ thích mèo kêu. Mèo rất vui!
```

======

```
Chạy code: truyền vào tham số: id. 

Bước 1 là khởi tạo cuộc thoại chung: 
- Đi qua từng dòng data và lấy nó cho vào trong API

JSON thu được dạng 

{
    "status": "CHAT",
    "text": [
        "Eating phở in the morning can be a great way to start the day. Bữa sáng với phở và một chút cà phê hoặc trà có thể giúp cậu cảm thấy sảng khoái và sẵn sàng cho ngày mới, cậu thường ăn phở ở nhà hay ở quán?"
    ],
    "conversation_id": "123456",
    "msg": "scuccess",
    "language": "vi",
    "process_time": 1.112640142440796,
    "SYSTEM_CONTEXT_VARIABLES": {},
    "task_idx": 0
}

Output excel : copy file input và 
tạo 1 cột: full log
tạo 1 cột: text_response
...

```