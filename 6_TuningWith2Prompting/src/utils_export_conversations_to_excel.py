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