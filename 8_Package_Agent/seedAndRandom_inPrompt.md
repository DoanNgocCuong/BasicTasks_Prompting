```
[bot 24] bài Agent. (Mặc dù trong sheet đã được fix cứng: temperature=0, ...). 
Khi test với cùng 1 start_message và user_first_message => Output vẫn trả ra đang khác nhau trong 2 lần chạy, nguyên nhân do đâu anh nhỉ, (theo lý thuyết fix cứng là nó ko chạy được kết quả). ??

{
  "max_tokens": 1024,
  "temperature": 0.0,
  "top_p": 1,
  "model": "gpt-4o-mini",
  "stream": false
}


Để kết quả cố định em nghĩ là sau mình fix cứng thêm full các tham số cho dễ testing ạ. 
        temperature=0,
        max_completion_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
---
anh @Đinh Hùng, anh @Minh Hoang Duc . 
```


