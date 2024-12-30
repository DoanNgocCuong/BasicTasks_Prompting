
Step 2: 
output

```
{
  "text": "{\"status\": 200, \"message\": \"Thành công!\", \"data\": {\"id\": \"20241218102838-2d03ed47\", \"text\": \"Hello\", \"audio_url\": \"https://tts-file-mgc-52.hacknao.edu.vn/data/tts_male_ha_v3/8b1a9953c4611296a827abf8c47804d7_2_1.mp3\"}}",
  "files": [],
  "json": []
}
```


Step 3: 

```
def main(arg1: str) -> dict:
    """
    Trích xuất 'audio_url' từ dữ liệu JSON phức tạp.

    Parameters:
    - arg1 (str): Chuỗi JSON đầu vào chứa các lớp lồng nhau.

    Returns:
    - dict: Một từ điển chứa khóa 'result' với giá trị là 'audio_url'.
    """
    # Bước 1: Phân tích cú pháp JSON
    data_dict = json.loads(arg1)
    
    # Bước 2: Trích xuất 'audio_url' từ lớp trong cùng
    audio_url = data_dict['data']['audio_url']
    
    return {
        "result": audio_url
    }
```

Output Variable: result - string. 


Input: string from step previous step
```
{
  "arg1": "{\"status\": 200, \"message\": \"Thành công!\", \"data\": {\"id\": \"20241218102838-2d03ed47\", \"text\": \"Hello\", \"audio_url\": \"https://tts-file-mgc-52.hacknao.edu.vn/data/tts_male_ha_v3/8b1a9953c4611296a827abf8c47804d7_2_1.mp3\"}}"
}
```
(Nếu bạn chọn Input là: json thì nó sẽ trả ra rỗng). 

Output
```

```



KẾT LUẬN: 
- INPUT: nó sẽ lấy value của cái keys mình chọn (chẳng hạn ở step 3: input chọn key là: text hay JSON thì là chọn dựa vào keys chứ không phải TYPE OF GÌ ĐÓ)...
- OUTPUT: nó sẽ lấy value của cái keys mình chọn (chẳng hạn ở step 3: output chọn key là: result thì là key `result` của cái return của function mình viết). 