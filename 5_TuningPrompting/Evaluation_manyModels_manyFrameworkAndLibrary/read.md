Hôm nay em có code thêm 1 đoạn để call được API của Grod. 
Em có thử Thư viện mới của thầy Andrew Ng: https://github.com/andrewyng/aisuite/blob/main/guides/
------
Tình cờ phát hiện được cái này khá hay ạ. 


Đánh giá xem chạy bằng `aisuite Andrew Ng` với `openai lib` thuần. 

```python
        start_time = time.time()
        try_count = 0
        while try_count < 3:
            try:
                print(f"DEBUG - Attempt {try_count + 1} to call OpenAI API")
                completion = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=chat_messages,   
                    temperature=0,
                    max_tokens=6000,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                end_time = time.time()
```


1. Với data: Đánh giá Prompt _Intent Detection: 
=> Output ngắn thì Aisuite Lib lại nhanh hơn đáng kể so với OpenAI Lib. 
2. Với data dài; Đánh giá prompt Data khách hàng 
=> Output dài thì OpenAI Lib gốc lại cho thấy hiệu quả tốt hơn. 

----
=> Với data output ngắn như bài Detection => Lựa chọn thư viện Aisuite vẫn là lựa chọn khá là ngon, thậm chí rất ngon. 


========
[Đánh giá ĐỘ CHÍNH XÁC và RESPONSE TIME của AiSuite Lib với openAI Lib Gốc]: Cho Data ngắn độ chính xác 99% Response time ngắn hơn 1/3 đến 1 nửa ++ còn với Prompt siêu dài Inputt Data siêu dài thì độ khớp chính xác giảm còn 95%, thời gian tăng từ 1/5 tới 1/4


prompt, input ngắn
```
PERCENTILE 50%	PERCENTILE 75%	PERCENTILE 90%	PERCENTILE 95%
0.53	0.59	0.72	1.0175
			
openAI			
0.74	1.01	1.325	1.6475
```

prompt, input dài
```
PERCENTILE 50%	PERCENTILE 75%	PERCENTILE 90%	PERCENTILE 95%
1.725	1.96	2.293	2.811
oppenAI			
PERCENTILE 50%	PERCENTILE 75%	PERCENTILE 90%	PERCENTILE 95%
1.425	1.6875	1.93	2.0745
```