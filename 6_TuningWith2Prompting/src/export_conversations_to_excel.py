import pandas as pd
import os

def export_conversations_to_excel(messages, output_path):
    """Export conversations to Excel file by appending
    
    Args:
        messages: List of conversation messages to append
        output_path: Path to output Excel file
    """
    # Kiểm tra xem có cột 'order' trong messages không
    if 'Order' not in messages[0]:
        print("Warning: 'Order' column not found in messages. It will be excluded from the export.")
    
    df_new = pd.DataFrame(messages, columns=[
        'Role', 
        'Content', 
        'Response Time',
        'RoleA Prompt',
        'RoleB Prompt',
        'useApiOrPrompt',
        'Full Log'
    ])
    
    if not os.path.exists(output_path):
        # Create new file if doesn't exist
        df_new.to_excel(output_path, index=False, engine='openpyxl')
        print(f"\nCreated new export file: {output_path}")
    else:
        # Always append to existing file
        with pd.ExcelWriter(output_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            # Get the last row in existing file
            existing_df = pd.read_excel(output_path, engine='openpyxl')
            start_row = len(existing_df) + 1
            
            # Write new data starting from the next row
            df_new.to_excel(writer, startrow=start_row, index=False, header=False)
            print(f"\nAppended new conversation data to: {output_path}") 