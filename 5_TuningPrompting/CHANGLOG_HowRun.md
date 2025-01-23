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
