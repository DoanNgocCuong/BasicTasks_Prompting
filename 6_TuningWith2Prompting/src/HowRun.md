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

python main.py --input '2PromptTune_GiaLapUserHVAppTheCoach_v1.1_promptPTY.xlsx' --output 'PTY.xlsx' --start-row 10 --num-rows 10

python main.py --input '2PromptTune_GiaLapUserTreCon_v1.3_100PikaLesson.xlsx' --output '100Pika.xlsx' --num-rows 10

main_withMaxWorkers.py --start-row 0 --num-rows 10 --input gen_nhanh.xlsx --output 68.xlsx --bot-id 68 --max-workers 4  

python main_withMaxWorkers.py --input '2PromptTune_GiaLapUserTreCon_v1.3_100PikaLesson.xlsx' --output '100Pika.xlsx' --num-rows 10

```

Các file này sử dụng: append dòng, nên bạn cứ chạy thoải mái nhá, nó sẽ tự log thêm dòng khi xong 1 row. 

========

### Get requirements.txt
```bash
pip freeze > requirements.txt
```