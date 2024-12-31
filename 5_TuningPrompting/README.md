


```
.\.venv\Scripts\Activate.ps1
```
--------------------
README

1. Set up your OpenAI API key:
   - Open PromptEng.py
   - Uncomment the line # openai.api_key = ''
   - Replace the empty string with your actual OpenAI API key

## Usage

2. Prepare your input Excel file:
   - The file should be named `input_data.xlsx`
   - The sheet name should be named `Prompting`
   - It should contain columns: 'order', 'prompt', and 'user_input'
   - Place it in the same directory as the script

3. Run the script:

-----------------

Prompting HandleTuning


Các bài toán đưa được về xài tool . 
- Cho data ở các cột => Phân nhóm học viên thành: Nhóm ngành nghề, nhóm chức vụ, và nhóm mục đích học tập. 
- Từ chunk các đoạn => tạo câu hỏi và câu trả lời.


CÁC SHEET CẦN RUN chỉ cần nó đặt ở đầu là được, vì cơ chế của code là tìm đến sheet đầu tiên (mặc định), chứ ko tìm theo tên sheet. 

### Example Input (input_data.xlsx)
| order | prompt                      | user_input         |
|-------|-----------------------------|--------------------|
| 1     | You are a helpful assistant. | Tell me a joke.    |
| 2     | You are a test creator.      | Create a question. |

### Example Output (output_data.xlsx)
| order | prompt                      | user_input         | assistant_response       | response_time |
|-------|-----------------------------|--------------------|--------------------------|---------------|
| 1     | You are a helpful assistant. | Tell me a joke.    | Why don't scientists...   | 2.50s         |
| 2     | You are a test creator.      | Create a question. | What is the capital...?   | 3.10s         |

-----------------------

### Notes:

- **Hướng 1**: Initially, copying all columns and attempting to process JSON using a find-replace method wasn't effective.
- **Hướng 2**: Processing each cell with code using a cursor worked well and was fast (~5 minutes).
- **Hướng 3**: Utilizing a large language model (LLM) to automate the extraction and formatting could be another approach (Chain of Prompt), making the process more efficient.

### Example Input

The input Excel file (`output_data.xlsx`) should have a column like the following:

| assistant_response |
|--------------------|
| {"Question": ["Question 1"], "Answer": ["Answer 1"]} |
| {"Question": ["Question 2"], "Answer": ["Answer 2"]} |

### Example Output

The output file (`processed_data.xlsx`) will contain the extracted questions and answers in two columns:

| Question   | Answer     |
|------------|------------|
| Question 1 | Answer 1   |
| Question 2 | Answer 2   |


- **Hướng 4** : JSON FORMAT:
{"Question": "", "Answer": ""},
{"Question": "", "Answer": ""}, 
{"Question": "<Question 1>", "Answer": ""}, 
{"Question": "<Question 2>", "Answer": ""}, 
...
{"Question": "<Question 16>", "Answer": ""},
]
