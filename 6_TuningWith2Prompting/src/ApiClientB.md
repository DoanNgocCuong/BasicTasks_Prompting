1. Bắt đầu cuộc hội thoại mới với việc call với 1 conversation_id mới. (conversation_id mới này sẽ được khởi tạo dựa vào gì đó để nó đặc trưng)
```
curl --location 'http://103.253.20.13:9400/personalized-ai-coach/api/v1/bot/initConversation' \
--header 'Content-Type: application/json' \
--data '{
    "bot_id": 3,
    "conversation_id": "123455677",
    "input_slots": {}
}'
```

Output 
```
{
    "status": 0,
    "msg": "Success",
    "conversation_id": "123455677"
}
```


2. Sử dụng conversation_id ở bên trên để bắt đầu cuộc hội thoại.
```bash
curl --location 'http://103.253.20.13:9400/personalized-ai-coach/api/v1/bot/webhook' \
--header 'Content-Type: application/json' \
--data '{
    "conversation_id": "123455677",
    "message": "sẵn sàng"
}'
```

Dựa vào conversation_id mà có history. 

Output 
```
{
    "status": "CHAT",
    "text": [
        "Chào em! Hôm nay chúng ta sẽ học cách mở rộng một câu nói để diễn đạt ý đầy đủ hơn. Em sẵn sàng chưa?"
    ],
    "conversation_id": "123455677",
    "msg": "scuccess",
    "language": "vi",
    "process_time": 0.00427699089050293,
    "SYSTEM_CONTEXT_VARIABLES": {},
    "task_idx": 0
}
```