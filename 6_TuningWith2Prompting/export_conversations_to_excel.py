import pandas as pd
from utils_export_conversations_to_excel import prepare_export_data, validate_export_path

def export_conversations_to_excel(all_messages, output_path):
    """Export all conversations and response times to an Excel file."""
    try:
        # Prepare data
        data = prepare_export_data(all_messages)
        
        # Validate output path
        output_path = validate_export_path(output_path)
        
        # Create DataFrame and export
        df_export = pd.DataFrame(data, 
                               columns=['Role', 'Content', 'Response_Time', 
                                      'RoleA_Prompt', 'RoleB_Prompt'])
        df_export.to_excel(output_path, index=False)
        print(f"Conversations exported to {output_path}")
        
    except PermissionError:
        print("Error: Please close the Excel file before saving.")
    except Exception as e:
        print(f"Error during export: {str(e)}") 