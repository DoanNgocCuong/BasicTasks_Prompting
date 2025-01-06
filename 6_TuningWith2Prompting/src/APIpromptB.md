```
curl --location 'http://103.253.20.13:9400/personalized-ai-coach/api/v1/bot/initConversation' \
--header 'Content-Type: application/json' \
--data '{
    "bot_id": 3,
    "conversation_id": "123455677",
    "input_slots": {}
}'
```

```bash
curl --location 'http://103.253.20.13:9400/personalized-ai-coach/api/v1/bot/webhook' \
--header 'Content-Type: application/json' \
--data '{
    "conversation_id": "123455677",
    "message": "sẵn sàng"
}'
```