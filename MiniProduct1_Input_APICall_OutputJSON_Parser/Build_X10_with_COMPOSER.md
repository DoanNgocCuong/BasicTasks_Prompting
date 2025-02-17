

### Problem 
1. Code run evaluation. 
Thấy 1 điểm chung: 
- For i in range từng dòng xong rồi chạy qua 1 API nào đó 
- Output ra rồi =>Parser nó ra, (có code parser full JSON rồi). 
- Các cột quan trọng : INPUT(input1, input2, input3, ...) -> OUTPUT(output1, output2, output3).
===
Đóng gói cho cả dạng: Prompting testing, Run API testing workflow, run API Fast response ? - Code này sẽ để ở đâu? 
=> để ở trong phần Tools? 
+, Nếu dạng response ra không phải JSON thì sao => thì ko cần làm. 
- Task Prompting testing (Input, Prompt với Input dạng JSON bắn qua API OpenAI, API OpenAI khác với API server thông thường, kiểu định dạng JSON khác nhau chẳng hạn , Output). => đưa về Crul => Output. 
- Dạng chạy benchmark model: Input là gì, input này cũng phải biến thành CRUL, xong CRUL này nó bắn ra output (tại sao ko cho crul lên trên sheet luôn mà cứ phải để mỗi input user  trên sheet còn CRUL trong code lại phải sủa) 
- Dùng cho dạng đánh giá fast model, Input JSON, CRUL, output JSON. 


======

### Solution:
Đi qua từng dòng và chạy CRUL . 

- input data gồm 1 cột: CRUL
- output file thì copy file input và thêm cột OUPUT. Cột OUTPUT nếu là text thì giữ nguyên, còn nếu là JSON thì JSON parser ra các cột trên file đó luôn. 
- Run đến đâu dòng update đến đấy. 