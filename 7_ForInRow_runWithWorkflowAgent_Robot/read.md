1. API của Workflow: 

```bash
curl --location 'http://103.253.20.13:9403/robot-ai-workflow/api/v1/bot/initConversation' \
--header 'Content-Type: application/json' \
--data '{
    "bot_id": 1,
    "conversation_id": "123455667",
    "input_slots": {}
}'
```

---

```bash
curl --location 'http://103.253.20.13:9403/robot-ai-workflow/api/v1/bot/webhook' \
--header 'Content-Type: application/json' \
--data '{
    "conversation_id": "123455667",
    "message": "Thích nấu cá",
    "history": [
        {
            "role": "assistant",
            "content": "Chào cậu! Hôm nay chúng ta sẽ học về chủ đề đồ ăn nhé! Các món ăn yêu thích của cậu là gì nào?"
        }
    ],
    "question_idx": 1
}'
```


=> For i in range() loop qua từng dòng code. 
=> 