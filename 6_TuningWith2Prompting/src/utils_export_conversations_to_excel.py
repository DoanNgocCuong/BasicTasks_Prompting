import pandas as pd
from pathlib import Path

def prepare_export_data(all_messages):
    """Prepare data for export"""
    print("\n=== Preparing to Export Data ===")
    print(f"Total messages to export: {len(all_messages)}")
    print("First few rows of data:")
    for i, msg in enumerate(all_messages[:3]):
        print(f"Row {i+1}: {msg}")
    return all_messages

def validate_export_path(output_path):
    """Validate export path"""
    output_path = str(output_path)
    if not output_path.endswith('.xlsx'):
        output_path += '.xlsx'
    return output_path

def export_conversations_to_excel(df, output_path):
    """Export DataFrame to Excel file"""
    output_path = validate_export_path(output_path)
    
    # Kiểm tra xem cột 'order' có tồn tại không
    if 'Order' in df.columns:
        print("Exporting data with 'Order' column.")
    else:
        print("Warning: 'Order' column not found in the DataFrame. It will be excluded from the export.")
    
    # Xuất dữ liệu ra Excel
    try:
        df.to_excel(output_path, index=False)
        print(f"Data exported successfully to {output_path}")
    except Exception as e:
        print(f"Error exporting data: {str(e)}") 