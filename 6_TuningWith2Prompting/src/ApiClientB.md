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

```
{
  "status": "END",
  "text": [
    "Xin lỗi, hiện tại hệ thống đang trong quá trình bảo trì và nâng cấp, anh chị vui lòng liên hệ lại sau"
  ],
  "conversation_id": "1736240300709",
  "msg": "scuccess",
  "language": null,
  "process_time": 0.4231572151184082,
  "SYSTEM_CONTEXT_VARIABLES": {},
  "task_idx": 1
}
```


3. Chú ý: 
- Khi xài trên giao diện UI, bản chất là call 2 API trên. 
+, Với init_message là: 'sẵn sàng' (được truyền trong API đó)
+, sau đó AI Assistant sẽ trả về 1 câu là câu được fix cứng. 
+, User nói thêm 1 câu. 
+, AI Assistant sẽ trả về 1 câu là câu được gen. 

TUY NHIÊN: CÂU AI ASSISTANT GEN ĐẦU TIÊN NÀY ĐÚNG RA LÀ KO TÍNH CÂU: 'sẵn sàng' (init_message) cơ. 

Thế mà qua test mình thấy: INIT_MESSAGE PHẢI TRÙNG NHAU THÌ VỚI first_message_user MỚI CHO KẾT QUẢ TRÙNG NHAU. 

---
# THAY 9400 SANG 9404
1 api TƯƠNG TỰ: https://documenter.getpostman.com/view/5776947/2sAY55ZxoJ

1. Init Conversation
```
curl --location 'http://103.253.20.13:9404/robot-ai-lesson/api/v1/bot/initConversation' \
--header 'Content-Type: application/json' \
--data '{
    "bot_id": 16,
    "conversation_id": "123456789",
    "input_slots": {}
}'
```


```
{
    "status": 0,
    "msg": "Success",
    "conversation_id": "123456789"
}
```

2. Webhook

```bash
curl --location 'http://103.253.20.13:9404/robot-ai-lesson/api/v1/bot/webhook' \
--header 'Content-Type: application/json' \
--data '{
    "conversation_id": "123456789",
    "message": "sẵn sàng"
}'
```

Output: 
```
{
    "status": "success",
    "text": [
        "This is the response from RoleB."
    ],
    "process_time": 0.123456
}
```

Full Output: 
```
{
    "status": "CHAT",
    "text": [
        "Giờ chúng ta sẽ luyện tập chọn cách dịch đúng của câu từ tiếng Việt sang tiếng Anh nhé! Mình cùng bắt đầu nha. "
    ],
    "record": {
        "CUR_TASK_STATUS": "CHAT",
        "NEXT_ACTION": 0
    },
    "conversation_id": "123456789",
    "input_slots": {},
    "logs": {
        "status": "CHAT",
        "text": [
            "Giờ chúng ta sẽ luyện tập chọn cách dịch đúng của câu từ tiếng Việt sang tiếng Anh nhé! Mình cùng bắt đầu nha. "
        ],
        "conversation_id": "123456789",
        "msg": "scuccess",
        "record": {
            "status": "CHAT",
            "CUR_INTENT": "fallback",
            "INTENT_PREDICT_LLM": null,
            "NEXT_ACTION": 1,
            "PRE_ACTION": null,
            "CUR_ACTION": "Giờ chúng ta sẽ luyện tập chọn cách dịch đúng của câu từ tiếng Việt sang tiếng Anh nhé! Mình cùng bắt đầu nha. ",
            "LOOP_COUNT": [
                {
                    "fallback": 1
                },
                {},
                {},
                {},
                {}
            ],
            "SYSTEM_SCORE_SUM": 0
        },
        "process_time": 0.003558635711669922
    },
    "process_time": 0.2216784954071045
}
```

Muốn lấy thêm các keys khác (chẳng hạn: key: LOOP_COUNT để tính toán , ... thì code thêm ở file: def_simulate_with_api.py nhé)