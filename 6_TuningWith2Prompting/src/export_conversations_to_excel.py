import pandas as pd
from utils_export_conversations_to_excel import prepare_export_data, validate_export_path

def export_conversations_to_excel(messages, output_path):
    """Export conversations to Excel file"""
    df = pd.DataFrame(messages, columns=[
        'Role', 
        'Content', 
        'Response Time',
        'RoleA Prompt',
        'RoleB Prompt',
        'useApiOrPrompt'  # Thêm cột useApiOrPrompt
    ])
    df.to_excel(output_path, index=False)
    print(f"\nExported conversations to: {output_path}") 