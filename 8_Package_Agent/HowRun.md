Run:
```bash
python main_v1.py --num-rows 2
```

```bash
python main.py --start-row 0 --num-rows 1
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


```bash
python main.py --num-rows 10 --bot-id 20 --input '2PromptingTuning_10Turns_new_v3.xlsx' --output 'id20.xlsx'
python main.py --num-rows 10 --bot-id 32 --input '2PromptingTuning_10Turns_new_v3.xlsx' --output 'id32.xlsx'

python main.py --num-rows 10 --bot-id 18 --input '2PromptingTuning_10Turns_new_v3.xlsx' --output 'id18.xlsx'
```