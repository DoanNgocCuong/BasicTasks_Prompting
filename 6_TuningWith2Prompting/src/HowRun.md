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
python main.py --num-rows 10 --bot-id 20 --input '2PromptingTuning_40Turns.xlsx' --output 'id20.xlsx'
python main.py --num-rows 10 --bot-id 32 --input '2PromptingTuning_40Turns.xlsx' --output 'id32.xlsx'
python main.py --num-rows 10 --bot-id 33 --input '2PromptingTuning_40Turns.xlsx' --output 'id33.xlsx'
python main.py --input '2PrompTune_GiaLapUserTreCon_v1.2_callBotID.xlsx' --output 'id105.xlsx'  --bot-id 105 --start-row 10 --num-rows 10
```