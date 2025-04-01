import pandas as pd
import os
import re

def remove_rows_with_phrases(input_file, output_file, phrases):
    """
    Remove rows from Excel file that contain any of the specified phrases
    and create a new file with removed rows and their removal reasons
    
    Args:
        input_file (str): Path to input Excel file
        output_file (str): Path to save filtered Excel file
        phrases (list): List of phrases to check for removal
    """
    # Read Excel file
    df = pd.read_excel(input_file)
    
    print(f"Original rows: {len(df)}")
    
    # Create a copy for removed rows
    removed_df = df.copy()
    removed_df['Lý do loại bỏ'] = ''
    
    def check_exact_word(text, phrase):
        # Tạo pattern để match từ hoàn chỉnh
        pattern = r'\b' + re.escape(phrase) + r'\b'
        return bool(re.search(pattern, str(text), re.IGNORECASE))
    
    # Create a mask for rows to keep
    mask = pd.Series(True, index=df.index)
    
    # Check each row
    for idx, row in df.iterrows():
        for phrase in phrases:
            # Kiểm tra từng cell trong row
            if any(check_exact_word(cell, phrase) for cell in row):
                mask[idx] = False
                removed_df.at[idx, 'Lý do loại bỏ'] = phrase
                break
    
    # Filter dataframes
    filtered_df = df[mask]
    removed_df = removed_df[~mask]
    
    # Save filtered data to Excel
    filtered_df.to_excel(output_file, index=False)
    
    # Save removed rows with reasons to a separate file
    removed_output = os.path.splitext(output_file)[0] + '_removed.xlsx'
    removed_df.to_excel(removed_output, index=False)
    
    print(f"Rows removed due to phrases: {len(removed_df)}")
    print(f"Final rows after filtering: {len(filtered_df)}")
    print(f"Filtered data saved to: {output_file}")
    print(f"Removed rows saved to: {removed_output}")

def main():
    # Define paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, 'input_data.xlsx')
    output_file = os.path.join(current_dir, 'output_data.xlsx')
    word_file = os.path.join(current_dir, 'word.txt')
    
    # Read phrases from word.txt
    phrases_to_remove = []
    with open(word_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Remove '- ' prefix and strip whitespace
            phrase = line.strip().replace('- ', '')
            if phrase:  # Only add non-empty phrases
                phrases_to_remove.append(phrase)
    
    # Process the file
    remove_rows_with_phrases(input_file, output_file, phrases_to_remove)

if __name__ == "__main__":
    main()