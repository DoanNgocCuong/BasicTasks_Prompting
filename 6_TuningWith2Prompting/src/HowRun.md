Run V1: 
```
python main_v1.py --rows 2
```

Input 
```
STT	roleA_prompt	roleB_prompt	initialConversationHistory	maxTurns
1	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant	"[
    {""role"": ""roleA"", ""content"": ""What is your name?""}
]"	2
2	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant	"[
    {""role"": ""roleB"", ""content"": ""What is your name?""}
]"	2

```

Output: 
```
Role	Content	Response_Time	RoleA_Prompt	RoleB_Prompt
roleA	What is your name?	1.12	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant
roleA	I am Cuong, your AI Assistant. How can I help you today?	0.75	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant
roleB	Hello Cuong! I'm Minh, your AI Assistant. How can I assist you today?	1.05	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant
roleA	Hello Minh! It seems like we have a fun mix-up here. I'm Cuong, your AI Assistant. How can I assist you today?	0.91	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant
roleB	Hello Cuong! It looks like we’re both AI Assistants here. How can I assist you today?	0	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant
Separator	-------------------	0		
roleB	What is your name?	0.77	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant
roleA	My name is Cuong, and I'm here to assist you! How can I help you today?	0.82	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant
roleB	Hi Cuong! I'm here to help you with any questions or tasks you have. What can I assist you with today?	1.24	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant
roleA	Hi there! It seems like you might have mixed up our roles a bit. I'm here to assist you! If you have any questions or tasks you need help with, feel free to ask. What can I do for you today?	1.64	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant
roleB	Thank you for the clarification, Cuong! I appreciate your willingness to assist. If you have any questions or topics you'd like to discuss, feel free to let me know. How can I help you today?	0	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant
Separator	-------------------	0		

```



Run V2: 

Trong pandas, khi đọc Excel file bằng `pd.read_excel()`, dòng đầu tiên (header row) mặc định được sử dụng làm tên cột và không được tính vào index của DataFrame.

Ví dụ với file Excel có cấu trúc:
```
roleA_prompt | roleB_prompt | maxTurns  (row 1 - header)
value1       | value2       | 3         (row 2 - index 0)
value3       | value4       | 4         (row 3 - index 1)
value5       | value6       | 5         (row 4 - index 2)
```

Nên khi bạn muốn xử lý từ row 3-5 trong Excel (không tính header), bạn sẽ dùng:
```bash
python main.py --use-api --start-row 2 --rows 3
```

Vì:
- Row 3 trong Excel = index 2 trong DataFrame
- Row 5 trong Excel = index 4 trong DataFrame

Code hiện tại đã xử lý đúng theo logic này rồi, không cần sửa gì thêm.
