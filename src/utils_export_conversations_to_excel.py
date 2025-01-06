import pandas as pd

def export_conversations_to_excel(messages, output_path, columns=None):
    """
    Export conversations to Excel file
    Args:
        messages: List of message data
        output_path: Path to output Excel file
        columns: List of column names (optional)
    """
    if columns is None:
        columns = ['Role', 'Content', 'Response_Time', 'RoleA_Prompt', 'RoleB_Prompt']
        
    df = pd.DataFrame(messages, columns=columns)
    df.to_excel(output_path, index=False)
    print(f"\nExported {len(messages)} messages to {output_path}")