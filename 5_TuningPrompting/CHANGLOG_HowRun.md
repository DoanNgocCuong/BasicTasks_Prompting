v1: version cơ bản 
v2: add History Message dạng JSON 
```JSON
[{"role":"assistant","content":"Chúng ta sẽ bắt đầu với cụm 'Thức dậy'. Hãy cùng mình nói cụm 'Thức dậy' bằng tiếng anh nha"},{"role":"user","content":"À, 'Brush teeth' hả?"},{"role":"assistant","content":"Nghe thú vị thế. Nhưng trước tiên cùng nhắc lại cụm 'Thức dậy' trước nhen: 'Wake up'"},{"role":"user","content":"wake up"},{"role":"assistant","content":"Đúng rồi, giờ chúng ta qua cụm tiếp theo nhé. Đánh răng."}]


```
v3: done v3_5_TuningPrompting: done v3 có aiSuite với openAI, Grod. Gemini thì triển riêng (do Gemini của Aisuite thì ko call qua GEMIN_API_KEY - 09/01/2025


---
v4: Update PromptTuning_OpenAI_v4_v2UpdateParseArguments.py
```
def parse_arguments():
    parser = argparse.ArgumentParser(description='Process conversations with OpenAI API')
    parser.add_argument('--num-rows', type=int, default=None,
                      help='Number of rows to process (default: all rows)')
    parser.add_argument('--input-file', type=str, default='input_data.xlsx',
                      help='Input Excel file path (default: input_data.xlsx)')
    parser.add_argument('--output-file', type=str, default='output_data_v2.xlsx',
                      help='Output Excel file path (default: output_data_v2.xlsx)')
    parser.add_argument('--sheet', type=str, default='dang2',
                      help='Excel sheet name to process (default: dang2)')
    return parser.parse_args()
```




=======

Now you can run the script with arguments like:
```bash
python PromptTuning_OpenAI_v4_v2UpdateParseArguments.py --sheet dang2 --num-rows 10 --input-file custom_input.xlsx --output-file custom_output.xlsx
```

Or use default values by running without arguments:
```bash
python PromptTuning_OpenAI_v4_v2UpdateParseArguments.py
```

====
Run v5: 
```bash
python PromptTuning_OpenAI_v5.py --batch-size 50 --max-workers 40
```



Mình chạy server công ty thử để max_workers = 20, 40 đã nhanh hơn trước 20-40 lần luôn rồi. 
Để max_workers = 2000 luôn -) => Kết quả là trong chưa đầy 1 phút bình thường được 1 requests thì mình đã thấy tới 300 dòng output => sau 3min lên tới 1000 dòng luôn rồi. 


---

Prompt siêu dài nha 
```bash
🎯 **Yêu cầu:**
- **Input:** Một câu tiếng Việt bất kỳ.
- **Output:** Một câu tiếng Việt **bị sai be sai bét**, mắc lỗi ở **nhiều chỗ** với ít nhất **3 loại lỗi phát âm** hoặc **chính tả** sau:

|--------------------------|-------------------------------------|----------------------------------------------|
| **Ngọng n - l**          | Lẫn lộn "n" và "l".                | "Làm lon lôn" thay "Làm non non".            |
| **Ngọng s - x**          | Lẫn lộn "s" và "x".                | "Sang xang" thay "Sang sang".                |
| **Ngọng ch - tr**        | Lẫn lộn "ch" và "tr".              | "Trời trăng" thay "Chơi chăng".              |
| **Ngọng d - gi - r**     | Lẫn lộn ba âm này.                 | "Rong rìa" thay "Giông giềng".               |
| **Ngọng t - c**          | Lẫn lộn âm cuối "t" và "c".        | "Mát" thay "Mác".                            |
| **Ngọng n/ng**           | Lẫn lộn giữa "n" và "ng".          | "Con nong" thay "Con nông".                 |
| **Sai âm cuối**          | Thiếu hoặc phát âm sai âm cuối.    | "Đang nấu cơn" thay "Đang nấu cơm".          |
| **Sai dấu**              | Thay đổi dấu thanh.                | "Cá chép" thay "Cá chẹp".                   |
| **Sai từ đồng âm**        | Sử dụng sai từ đồng âm khác nghĩa. | "Hát cao su" thay "Hát cao".                |
| **Lỗi chính tả thường gặp** | Viết sai từ phổ biến.             | "Mỉnh" thay "Mình", "bít" thay "biết".       |
| **Cấu trúc câu lộn xộn**  | Hoán đổi vị trí từ sai ngữ pháp.  | "Cơm ăn tôi no" thay "Tôi ăn cơm no".        |

---

📌 **Quy tắc output:**
- **Output PHẢI LÀ 1 CÂU DUY NHẤT**, nhưng **sai be sai bét** ở nhiều chỗ.  
- Câu **phải chứa ít nhất 3 dạng lỗi khác nhau** từ bảng trên.  
- **Ý nghĩa gốc của câu vẫn nhận ra được**, dù bị sai nhiều chỗ.  
- **Tự thêm từ hoặc thay đổi cấu trúc câu** nếu cần để đạt yêu cầu sai toàn diện.  
- **Lỗi phải xuất hiện liên tục, trải đều trong câu**, không chỉ tập trung ở đầu hoặc cuối câu.

---

📝 **Ví dụ minh họa:**

1️⃣ **Input:** "Tôi đang nấu cơm ở nhà."  
   ➡️ **Output:**  
   `"Tôi đăng nấu cơn ở nà lò."`  
   (*Sai âm cuối + ngọng n/l + sai dấu + lỗi chính tả*)  

---

2️⃣ **Input:** "Trời hôm nay thật đẹp."  
   ➡️ **Output:**  
   `"Chời hôn nai thậc đẹc."`  
   (*Ngọng ch/tr + sai dấu + t/c + sai âm cuối*)  

---

3️⃣ **Input:** "Bạn sang nhà tôi chơi nhé."  
   ➡️ **Output:**  
   `"Bặn xang nhà tơi chời nhẻ."`  
   (*Ngọng n/l + s/x + ch/tr + sai dấu + lỗi chính tả*)  

---

4️⃣ **Input:** "Rau này rất ngon."  
   ➡️ **Output:**  
   `"Dau nai rấc ngong."`  
   (*Ngọng r/d + t/c + sai âm cuối + sai chính tả*)  

---

5️⃣ **Input:** "Tối nay chúng ta sẽ ăn cơm gà nướng."  
   ➡️ **Output:**  
   `"Tới nai chún ta xẽ ăn cơn cà ngước."`  
   (*Ngọng t/c + ch/tr + s/x + sai âm cuối + sai dấu*)  

---

6️⃣ **Input:** "Anh ấy học rất chăm chỉ."  
   ➡️ **Output:**  
   `"Anh ấy học rấc chằm chỉ."`  
   (*Sai âm cuối + ngọng t/c + ch/tr*)  

---

7️⃣ **Input:** "Cô giáo đang giảng bài rất hay."  
   ➡️ **Output:**  
   `"Cô dao đăng rảng bài rấc hay."`  
   (*Ngọng d/gi/r + sai âm cuối + t/c*)  

---

8️⃣ **Input:** "Chúng tôi đi chợ mua rau xanh."  
   ➡️ **Output:**  
   `"Chún tơi đi chợ mua dau xanh."`  
   (*Ch/tr + ngọng r/d + s/x + sai âm cuối*)  

---

🎛 **Yêu cầu bổ sung (nếu cần):**
- Nếu muốn thêm **lỗi ngữ pháp** như lặp từ hoặc cấu trúc câu sai, có thể xuất hiện:  
  - **"Tôi tôi đã ăn ăn cơm rồi."** (*Lặp từ*)  
  - **"Cơm ăn tôi rồi no."** (*Cấu trúc câu lộn xộn*)  

---

📢 **Tóm tắt yêu cầu chính:**  
1️⃣ Câu đầu ra PHẢI **sai toàn diện** với **nhiều lỗi phát âm và chính tả**.  
2️⃣ **Không cần giữ câu quá sát với bản gốc**, miễn **nghe vẫn nhận ra ý chính**.  
3️⃣ **Tự động thêm từ, hoán đổi trật tự từ**, miễn đảm bảo **đủ lỗi sai**.

---

📩 **Nếu cần thêm loại lỗi cụ thể hoặc tăng độ khó (ví dụ: lỗi ngữ pháp phức tạp, từ đồng âm gây hiểu nhầm...), hãy cho mình biết nhé!** 😊

RESPONSE FORMAT: only sentence (not include other character)
```

Để max_workers = 2000 là một ý tưởng không tốt vì nhiều lý do:

1. **Giới hạn tự động:**
```python
def optimize_batch_parameters(total_rows: int, args):
    # Tối ưu max_workers
    recommended_workers = min(
        resources['cpu_count'],  # Giới hạn bởi số CPU cores
        int(8 * (100 - resources['cpu_percent']) / 100),  # Giới hạn bởi CPU usage
        int(resources['available_memory_gb'])  # Giới hạn bởi RAM
    )
```
Code sẽ tự động giảm số workers xuống mức an toàn, dù bạn set 2000.

2. **Các vấn đề có thể xảy ra:**
- **Rate Limits của OpenAI API**: Quá nhiều requests đồng thời sẽ bị limit
- **Memory Overflow**: Mỗi thread tiêu tốn memory
- **Thread Overhead**: Quá nhiều threads sẽ làm hệ thống chậm đi
- **Network Issues**: Có thể gây quá tải network

3. **Khuyến nghị:**
- Nên để max_workers trong khoảng 2-3 lần số CPU cores
- Với 96 cores, nên để max_workers khoảng 40-50 là hợp lý
- Tăng batch_size thay vì tăng max_workers nếu muốn xử lý nhanh hơn

4. **Cách tính workers hợp lý:**
```python
recommended_workers = min(
    CPU_CORES,           # Ví dụ: 96
    AVAILABLE_RAM_GB,    # Ví dụ: 140
    MAX_API_CONCURRENT   # Giới hạn của OpenAI API
)
```

**Kết luận:** Đừng set max_workers = 2000. Hãy để hệ thống tự optimize hoặc set một giá trị hợp lý (40-50) để đảm bảo hiệu suất tốt nhất.
