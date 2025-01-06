```
[
    {"role": "roleA", "content": "Hello"},
    {"role": "roleB", "content": "Hi, how can I help?"},
    ...
]
```


```
STT	createUserQuestion_prompt	AIAssistantResponse_prompt	conversationHistory	max_response
1	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant	"[
    {""role"": ""roleA"", ""content"": ""What is your name?""},
    {""role"": ""roleB"", ""content"": ""What is your name?""}
]"	2
2	You are Cuong. You are AI Assistant	You are Minh. You are AI Assistant	"[
    {""role"": ""roleB"", ""content"": ""What is your name?""},
    {""role"": ""roleA"", ""content"": ""What is your name?""}
]"	2
```