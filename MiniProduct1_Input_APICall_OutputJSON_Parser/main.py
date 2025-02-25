import json
import pandas as pd
import time
from pathlib import Path
import argparse
import logging
import requests
import re

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def is_json(text):
    try:
        json.loads(text)
        return True
    except:
        return False

def execute_curl(curl_command):
    """Execute CURL command and return response"""
    try:
        # Parse CURL command
        headers = {}
        data = None
        method = 'GET'
        
        # Split command into lines and process each part
        parts = curl_command.replace('\\', '').split('\n')
        
        # Process first line to get URL
        url_line = parts[0].strip()
        # New pattern that handles URLs with or without quotes
        url_match = re.search(r"curl\s+['\"]?(.*?)['\"]?\s*$", url_line)
        if not url_match:
            return "Error: Could not parse URL from CURL command"
        url = url_match.group(1).strip()
        
        # Process remaining lines for headers and data
        current_data = []
        reading_data = False
        
        for part in parts[1:]:
            part = part.strip()
            if not part:
                continue
                
            # Parse headers
            if '-H' in part or '--header' in part:
                header_match = re.search(r"-H\s+['\"](.+?)['\"]|--header\s+['\"](.+?)['\"]", part)
                if header_match:
                    header_str = (header_match.group(1) or header_match.group(2)).replace('""', '"')
                    if ':' in header_str:
                        key, value = header_str.split(':', 1)
                        headers[key.strip()] = value.strip()
                continue
            
            # Start collecting data
            if '-d' in part or '--data' in part:
                reading_data = True
                data_part = re.sub(r"^-d\s+['\"]|^--data\s+['\"]", "", part)
                current_data.append(data_part)
                continue
                
            # Continue collecting data if we're in data mode
            if reading_data:
                current_data.append(part)
        
        # Join and clean data if we collected any
        if current_data:
            method = 'POST'
            data = ''.join(current_data)
            # Clean up the data
            data = data.strip("'\"")
            data = data.replace('""', '"')  # Replace double escaped quotes
            
        # Make the request
        if method == 'GET':
            response = requests.get(url, headers=headers)
        else:
            response = requests.post(url, headers=headers, data=data)
            
        return response.text
    except Exception as e:
        return f"Error executing CURL: {str(e)}"

def parse_output(output_text):
    """Parse output if it's JSON, otherwise return as is"""
    if is_json(output_text):
        try:
            parsed_json = json.loads(output_text)
            return json.dumps(parsed_json, indent=2)  # Pretty print JSON
        except json.JSONDecodeError as e:
            return f"JSON parsing error: {str(e)}"
    return output_text  # Return as is if not JSON

def process_row(crul_command):
    """Process a single row of data"""
    # Check if CURL command is valid
    if pd.isna(crul_command) or not isinstance(crul_command, str):
        print(f"\n=== Invalid CURL Command ===")
        print(f"Found invalid value: {crul_command}")
        return None, None
        
    print(f"\n=== Processing Input ===")
    print(f"CRUL: {crul_command[:100]}...")
    
    # Execute CRUL command
    output = execute_curl(crul_command)
    print("\n=== Raw Output ===")
    print(output[:500] + "..." if len(output) > 500 else output)
    
    # Parse output if it's JSON
    parsed_output = parse_output(output)
    if is_json(output):
        print("\n=== Parsed JSON Output ===")
        print(parsed_output)
    
    return output, parsed_output

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

def main():
    args = parse_arguments()
    
    # Define the base paths
    SCRIPTS_FOLDER = Path(__file__).parent
    INPUT_FILE = SCRIPTS_FOLDER / args.input_file
    OUTPUT_FILE = SCRIPTS_FOLDER / args.output_file

    # Read input Excel file
    try:
        df_input = pd.read_excel(INPUT_FILE, sheet_name=args.sheet)
    except Exception as e:
        logger.error(f"Error reading input file: {str(e)}")
        return

    # Verify required column exists
    if 'CRUL' not in df_input.columns:
        logger.error("Missing required column 'CRUL'")
        return

    # Convert 1-based to 0-based indexing and validate row ranges
    start_idx = args.start_row - 1
    # If end_row is None or greater than available rows, use the last row
    end_idx = min(args.end_row - 1 if args.end_row is not None else len(df_input) - 1, 
                  len(df_input) - 1)
    
    if start_idx < 0 or start_idx >= len(df_input):
        logger.error(f"Start row {args.start_row} is out of range. Valid range: 1 to {len(df_input)}")
        return
    
    # Create output DataFrame by copying input
    df_output = df_input.copy()

    # Process specified rows and update immediately
    for index in range(start_idx, end_idx + 1):
        print(f"\n{'='*50}")
        print(f"Processing row {index + 1} of {end_idx + 1}")
        print(f"{'='*50}")
        
        CRUL_command = df_input.iloc[index]['CRUL']
        
        # Process the row
        output, parsed_output = process_row(CRUL_command)
        
        # Skip if invalid CURL command
        if output is None:
            print(f"\nSkipping row {index + 1} due to invalid CURL command")
            continue
        
        if is_json(output):
            # If output is JSON, parse it and add columns
            try:
                json_data = json.loads(output)
                if isinstance(json_data, dict):
                    print("\n=== Adding JSON columns ===")
                    # Store the raw response output
                    df_output.loc[index, 'Raw_Output'] = output
                    # Add JSON columns
                    for key, value in json_data.items():
                        col_name = f'JSON_{key}'
                        df_output.loc[index, col_name] = str(value)
                        print(f"Added column '{col_name}' with value: {str(value)[:100]}...")
            except Exception as e:
                logger.error(f"Error parsing JSON at row {index}: {str(e)}")
        else:
            # If not JSON, store raw response output
            df_output.loc[index, 'Raw_Output'] = output
            print("\n=== Stored raw response output ===")

        # Save after each row
        try:
            df_output.to_excel(OUTPUT_FILE, index=False)
            print(f"\n✓ Successfully updated row {index + 1} and saved to '{OUTPUT_FILE}'")
        except PermissionError:
            print(f"\n❌ Error: File '{OUTPUT_FILE}' is open. Please close it and try again.")
            return
        except Exception as e:
            print(f"\n❌ Error saving output file: {str(e)}")
            return

    print(f"\n{'='*50}")
    print("Processing completed successfully!")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()