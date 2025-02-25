```

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process input and CRUL commands')
    parser.add_argument('--input-file', type=str, default='input_data.xlsx',
                      help='Input Excel file path (default: input_data.xlsx)')
    parser.add_argument('--output-file', type=str, default='output_data.xlsx',
                      help='Output Excel file path (default: output_data.xlsx)')
    parser.add_argument('--sheet', type=str, default='Trang tính1',
                      help='Excel sheet name to process (default: Trang tính1)')
    parser.add_argument('--start-row', type=int, default=1,
                      help='Start row number (1-based indexing, default: 1)')
    parser.add_argument('--end-row', type=int, default=None,
                      help='End row number (1-based indexing, default: last row)')
    return parser.parse_args()
```
