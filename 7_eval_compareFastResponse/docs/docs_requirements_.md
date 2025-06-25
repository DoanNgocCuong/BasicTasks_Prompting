```
curl --location 'http://103.253.20.30:8990/fast_response/generate' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
  "conversations": [
    {"role": "assistant", "content": "Hôm nay, tớ mới tìm hiểu được về 5 loài động vật to nhất trên Trái Đất. Cậu có tò mò không?"},
    {"role": "user", "content": "tớ chán rồi"}
  ],
  "system_prompt": "You are QuickReact: detect the emotion in the latest message and reply instantly in its same language (English or Vietnamese) using 1-8 words (≤60 chars), keep it short enough with a friendly informal tone that mirrors and empathizes with that feeling (sad → soothe, happy → cheer, worried → reassure; emojis/!/? welcome); output only that text—never answer the question, just buy time until the main reply arrives.",
  "model_name": "Qwen/Qwen3-4B",
  "temperature": 0.8,
  "top_p": 1
}
'
curl --location 'https://robot-api.hacknao.edu.vn/robot/api/v1/admin/conversations/8532' \
--header 'X-API-Key: {{token}}'
id bài 358, 359, 362
3 bài này thôi

Output a cần là có 1 version để deploy production (chỉ cần same same hoặc hơn hiện tại 1 chút) kèm các tiêu chí để bên đấy đánh giá xem fast response ntn là tốt, sau đó tối ưu prompt


```

---

1. Tạo file get_data_conversation.py
Call API lấy data JSON lưu vào folder input 
```bash
curl --location 'https://robot-api.hacknao.edu.vn/robot/api/v1/admin/conversations/8532' \
--header 'X-API-Key: {{token}}'

2. Tạo file processed.py

- tiền xử lý dữ liệu JSON sang dạng file processed.xlsx
```bash
{
    "status": 200,
    "message": "Success",
    "data": [
        {
            "character": "BOT_RESPONSE_CONVERSATION",
            "content": "Hôm nay cậu thích nói về chủ đề gì?",
            "audio": "http://tts-file-mgc-52.hacknao.edu.vn/data/tts_female_linh_v1/0fe92cd051dd3dbd7bc3a63210ff37c0_3_1.0.mp3"
        },
        {
            "character": "USER",
            "content": "-",
            "audio": "https://smedia.stepup.edu.vn/robot/audio/user/250319/201ce9ee-3d71-727a-c9a6-575bc5700d07_1742373779025.wav"
        },
        {
            "character": "FAST_RESPONSE",
            "content": "Hình như có ai đó đang chơi trò im lặng là vàng nè!",
            "audio": "http://tts-file-mgc-42.hacknao.edu.vn/data/tts_female_linh_v1/2201f69493836d57aad579a77f2e8ac4_3_1.0.mp3"
        },
        {
            "character": "BOT_RESPONSE_CONVERSATION",
            "content": "Tớ chưa nghe rõ, cậu thích nói về chủ đề gì nhỉ ",
            "audio": "http://tts-file-mgc-52.hacknao.edu.vn/data/tts_female_linh_v1/8f1bdf964979895d54d881c602d9e16a_3_1.0.mp3"
        },
        {
            "character": "USER",
            "content": "Don't worry, it will be fine.",
            "audio": "https://smedia.stepup.edu.vn/robot/audio/user/250319/201ce9ee-3d71-727a-c9a6-575bc5700d07_1742373793616.wav"
        },
        {
            "character": "FAST_RESPONSE",
            "content": "Để Pika xem thử nào!",
            "audio": "http://tts-file-mgc-52.hacknao.edu.vn/data/tts_female_linh_v1/f96c8bfed1327a95548d7e4b3e3a0198_3_1.0.mp3"
        },
        {
            "character": "BOT_RESPONSE_CONVERSATION",
            "content": "Ồ thật thú vị",
            "audio": "http://tts-file-mgc-52.hacknao.edu.vn/data/tts_female_linh_v1/99157ab92c51648798b996868ebe0dd4_3_1.0.mp3"
        },
        {
            "character": "BOT_RESPONSE_CONVERSATION",
            "content": "Hôm nay cậu thích nói về chủ đề gì",
            "audio": "http://tts-file-mgc-52.hacknao.edu.vn/data/tts_female_linh_v1/d1b0fbd2c221c5eff3661a29123e2203_3_1.0.mp3"
        },
        {
            "character": "USER",
            "content": "-",
            "audio": "https://smedia.stepup.edu.vn/robot/audio/user/250319/201ce9ee-3d71-727a-c9a6-575bc5700d07_1742373810200.wav"
        },
        {
            "character": "FAST_RESPONSE",
            "content": "Yên ắng quá. Pika chỉ còn tiếng gió thổi qua thôi nè!",
            "audio": "http://tts-file-mgc-52.hacknao.edu.vn/data/tts_female_linh_v1/5f0fd2a0e0c4baf38cd7bfa62829d746_3_1.0.mp3"
        },
        {
            "character": "BOT_RESPONSE_CONVERSATION",
            "content": "Tớ chưa nghe rõ, cậu nói lại xem",
            "audio": "http://tts-file-mgc-52.hacknao.edu.vn/data/tts_female_linh_v1/88a4d361ed12a2ae28115b39c6c5029b_3_1.0.mp3"
        },
        {
            "character": "USER",
            "content": "I say it's a pet.",
            "audio": "https://smedia.stepup.edu.vn/robot/audio/user/250319/201ce9ee-3d71-727a-c9a6-575bc5700d07_1742373823855.wav"
        },
        {
            "character": "FAST_RESPONSE",
            "content": "Let me take a closer look at that!",
            "audio": "http://tts-file-mgc-52.hacknao.edu.vn/data/tts_female_linh_v1/94e4f483fb762b572a5c65709217074a_3_1.0.mp3"
        },
        {
            "character": "BOT_RESPONSE_CONVERSATION",
            "content": "Chính xác, tiếp theo nói fun facts nhé",
            "audio": "http://tts-file-mgc-42.hacknao.edu.vn/data/tts_female_linh_v1/252bb4f1d9b94d3faee34d7331c37e8c_3_1.0.mp3"
        },
        {
            "character": "USER",
            "content": "So now my project can...",
            "audio": "https://smedia.stepup.edu.vn/robot/audio/user/250319/201ce9ee-3d71-727a-c9a6-575bc5700d07_1742373837277.wav"
        },
        {
            "character": "FAST_RESPONSE",
            "content": "That sounds like a great answer!",
            "audio": "http://tts-file-mgc-42.hacknao.edu.vn/data/tts_female_linh_v1/11b3767d33db4cb8b902cfe0dfaa78f1_3_1.0.mp3"
        },
        {
            "character": "BOT_RESPONSE_CONVERSATION",
            "content": "Nói lại fun facts nhé",
            "audio": "http://tts-file-mgc-52.hacknao.edu.vn/data/tts_female_linh_v1/9decf218e69be71c9fd7e04c5e1e01df_3_1.0.mp3"
        },
        {
            "character": "USER",
            "content": "Fun fight!",
            "audio": "https://smedia.stepup.edu.vn/robot/audio/user/250319/201ce9ee-3d71-727a-c9a6-575bc5700d07_1742373849967.wav"
        },
        {
            "character": "FAST_RESPONSE",
            "content": "Thú vị ghê*#*#",
            "audio": "http://tts-file-mgc-52.hacknao.edu.vn/data/tts_female_linh_v1/06e2e345c051493b18dbaf5bb169fcbe_3_1.0.mp3"
        },
        {
            "character": "BOT_RESPONSE_CONVERSATION",
            "content": "Chuẩn luôn bye bye",
            "audio": "http://tts-file-mgc-52.hacknao.edu.vn/data/tts_female_linh_v1/115753e2eae47bb756bbae79afb122eb_3_1.0.mp3"
        }
    ]
}
```

Chia processed thành 3 cột: 
- Cột: BOT_RESPONSE_CONVERSATION_with_USER
```bash
[
    {"role": "assistant", "content": "Hôm nay, tớ mới tìm hiểu được về 5 loài động vật to nhất trên Trái Đất. Cậu có tò mò không?"},
    {"role": "user", "content": "tớ chán rồi"}
  ]
```

```bash
[
    {"role": "assistant", "content": "Hôm nay, tớ mới tìm hiểu được về 5 loài động vật to nhất trên Trái Đất. Cậu có tò mò không?"},
    {"role": "user", "content": "tớ chán rồi"}, 
   {"role": "assistant", "content": "..."},
    {"role": "user", "content": "..."}, 
  ]

```

- Cột FAST_RESPONSE_next
- Cột BOT_RESPONSE_CONVERSATION_next


3. Code run_eval_api_fast_response.py Chạy lần lượt data từng dòng của cột: BOT_RESPONSE_CONVERSATION_with_USER tronbg file data
thông qua API đã thảo luận, để: 
=> Output copy file này ra 1 file khác và thêm 1 cột: generated_ai , đặt tên file là output_eval.xlsx

4. Code File main.py sẽ điều phối toàn bộ luồng, 

input là: id hoặc list id. ()
output là: excel với mỗi id là 1 sheet 

> Các cách để input đơn giản, sau dễ scale: 

4.1 Nhận trực tiếp list ID qua command line:

Nhập 1 hoặc nhiều ID (phân tách bằng khoảng trắng).
Ví dụ:
Copypython main.py 358 359 362
Trong code dùng sys.argv hoặc argparse để nhận list này.
(Tuỳ chọn) Nhận từ file văn bản khi list quá dài:

4.2 Cho phép chỉ định file chứa danh sách ID (mỗi ID một dòng).
Ví dụ:
Copypython main.py --id_file ids.txt
Trong code kiểm tra nếu có --id_file thì đọc ID từ file, nếu không thì lấy từ command line.
(Tuỳ chọn) Kết hợp cả hai:

4.3 Nhập nhanh 1 vài ID, hoặc nhập file nếu cần scale lớn.
Có thể ưu tiên file nếu cả hai cùng nhập.
