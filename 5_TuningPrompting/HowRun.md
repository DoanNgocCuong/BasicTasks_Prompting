# Vào môi trường ảo: 
```bash
python -m venv myvenv

# Trên Windows
.\myvenv\Scripts\activate

# Trên Linux/Mac
source myvenv/bin/activate
```

# Basic run with default parameters
python PromptTuning_OpenAI_v5_BatchSize_NumWorkers.py

# Run with custom input/output files
python PromptTuning_OpenAI_v5_BatchSize_NumWorkers.py --input-file custom_input.xlsx --output-file custom_output.xlsx

# Run with specific number of rows
python PromptTuning_OpenAI_v5_BatchSize_NumWorkers.py --num-rows 100

# Run with custom sheet name
python PromptTuning_OpenAI_v5_BatchSize_NumWorkers.py --sheet "Sheet1"

# Run with custom batch size and workers
python PromptTuning_OpenAI_v5_BatchSize_NumWorkers.py --batch-size 8 --max-workers 6

# Run with all custom parameters
python PromptTuning_OpenAI_v5_BatchSize_NumWorkers.py \
  --input-file data.xlsx \
  --output-file results.xlsx \
  --sheet "MySheet" \
  --num-rows 50 \
  --batch-size 10 \
  --max-workers 8


```bash
def parse_arguments():
    parser = argparse.ArgumentParser(description='Process conversations with OpenAI API')
    parser.add_argument('--num-rows', type=int, default=None,
                      help='Number of rows to process (default: all rows)')
    parser.add_argument('--input-file', type=str, default='input_data.xlsx',
                      help='Input Excel file path (default: input_data.xlsx)')
    parser.add_argument('--output-file', type=str, default='output_data_v2.xlsx',
                      help='Output Excel file path (default: output_data_v2.xlsx)')
    parser.add_argument('--sheet', type=str, default='Trang tính1',
                      help='Excel sheet name to process (default: Trang tính1)')
    parser.add_argument('--batch-size', type=int, default=4,
                      help='Number of items to process in each batch (default: 4)')
    parser.add_argument('--max-workers', type=int, default=4,
                      help='Maximum number of worker threads (default: 4)')
    return parser.parse_args()
```