import pandas as pd
import re
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("task_description_extractor.log"),
        logging.StreamHandler()
    ]
)

def extract_task_descriptions(input_file):
    """
    Extract task descriptions from Excel file and save to a new Excel file.
    
    The function:
    1. Opens each sheet in the Excel file
    2. Finds the column with header "SYSTEM_TASK_DESCRIPTION"
    3. Extracts text containing "Task Description" (case insensitive) from the first row
    4. Saves results to a new Excel file
    """
    # Check if file exists
    if not os.path.exists(input_file):
        logging.error(f"File '{input_file}' not found.")
        return
    
    # Read the Excel file
    try:
        logging.info(f"Opening Excel file: {input_file}")
        xl = pd.ExcelFile(input_file)
        logging.info(f"Found {len(xl.sheet_names)} sheets: {', '.join(xl.sheet_names)}")
    except Exception as e:
        logging.error(f"Error opening Excel file: {e}")
        return
    
    # Prepare output data
    results = []
    
    # Process each sheet
    for sheet_name in xl.sheet_names:
        logging.info(f"Processing sheet: '{sheet_name}'")
        try:
            df = pd.read_excel(input_file, sheet_name=sheet_name)
            logging.info(f"Sheet '{sheet_name}' has {len(df.columns)} columns: {', '.join(str(col) for col in df.columns)}")
            
            # Find the column with SYSTEM_TASK_DESCRIPTION
            system_task_col = None
            for col in df.columns:
                if col == "SYSTEM_TASK_DESCRIPTION":
                    system_task_col = col
                    logging.info(f"Found 'SYSTEM_TASK_DESCRIPTION' column in sheet '{sheet_name}'")
                    break
            
            if system_task_col is None:
                logging.warning(f"No 'SYSTEM_TASK_DESCRIPTION' column found in sheet '{sheet_name}'. Skipping this sheet.")
                continue
            
            # Get the first non-empty value in the column
            first_row = None
            for i, value in enumerate(df[system_task_col]):
                if isinstance(value, str) and value.strip():
                    first_row = value.strip()
                    logging.info(f"Found first non-empty value in row {i+2}")  # +2 for Excel row number (header + 1-based)
                    logging.debug(f"Value: {first_row[:100]}...")  # Log first 100 chars
                    break
            
            if first_row is None:
                logging.warning(f"No data found in 'SYSTEM_TASK_DESCRIPTION' column in sheet '{sheet_name}'. Skipping this sheet.")
                continue
            
            # Extract text containing "Task Description" (case insensitive)
            pattern = re.compile(r'task description', re.IGNORECASE)
            match = pattern.search(first_row)
            
            if match:
                # Find the start and end of the task description section
                start_pos = match.start()
                
                # Extract the task description text
                task_description_text = first_row[start_pos:]
                logging.info(f"Found 'Task Description' keyword at position {start_pos}")
                logging.debug(f"Extracted text: {task_description_text[:100]}...")  # Log first 100 chars
                
                results.append({
                    'Sheet': sheet_name,
                    'TASK_DESCRIPTION': task_description_text
                })
                logging.info(f"Added task description from sheet '{sheet_name}' to results")
            else:
                logging.warning(f"No 'Task Description' keyword found in sheet '{sheet_name}'. Skipping this sheet.")
        
        except Exception as e:
            logging.error(f"Error processing sheet '{sheet_name}': {e}")
    
    # Save results to a new Excel file
    if results:
        output_file = "Extracted_TaskDescriptions.xlsx"
        output_df = pd.DataFrame(results)
        output_df.to_excel(output_file, index=False)
        logging.info(f"Results saved to '{output_file}' with {len(results)} task descriptions")
        
        # Print summary
        logging.info("\nExtraction Summary:")
        logging.info(f"Total sheets processed: {len(xl.sheet_names)}")
        logging.info(f"Sheets with task descriptions found: {len(results)}")
        logging.info(f"Sheets skipped: {len(xl.sheet_names) - len(results)}")
    else:
        logging.warning("No task descriptions found in any sheet.")

if __name__ == "__main__":
    input_file = "1. Personalized AI Coach - Thiết lập Agent.xlsx"
    logging.info("Starting task description extraction process")
    extract_task_descriptions(input_file)
    logging.info("Extraction process completed") 