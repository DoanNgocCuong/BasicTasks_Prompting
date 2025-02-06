from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
from def_ApiClientB import AICoachAPI
from export_conversations_to_excel import export_conversations_to_excel
from def_simulate_with_openai import simulate_with_openai
from def_simulate_with_api import simulate_with_api

# Load environment variables
load_dotenv()

# Get the directory containing the script
SCRIPT_DIR = Path(__file__).parent

app = FastAPI()

class ProcessingRequest(BaseModel):
    start_row: int | None = None
    num_rows: int | None = None
    input_file: str = '2PromptingTuning.xlsx'
    output_file: str = 'result.xlsx'
    bot_id: int = 31

def init_new_conversation(use_api=False, bot_id=31):
    """Initialize new clients and conversation for each row"""
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    api_client = None
    if use_api:
        api_client = AICoachAPI(bot_id=bot_id)
        if not api_client.init_conversation():
            raise HTTPException(status_code=500, detail="Failed to initialize API conversation")
    
    return openai_client, api_client

@app.post("/process-conversations")
async def process_conversations(request: ProcessingRequest):
    try:
        input_path = SCRIPT_DIR / request.input_file
        output_path = SCRIPT_DIR / request.output_file

        if not input_path.exists():
            raise HTTPException(status_code=404, detail=f"Input file not found: {input_path}")

        # Load data
        df = pd.read_excel(input_path)
        total_rows = len(df)
        
        # Calculate rows to process
        start_idx = request.start_row if request.start_row is not None else 0
        end_idx = min(start_idx + request.num_rows, total_rows) if request.num_rows else total_rows
        
        processed_rows = []
        
        for index, row in df.iloc[start_idx:end_idx].iterrows():
            use_api = str(row['useApiOrPrompt']).lower() == 'api'
            
            # Initialize new conversation for each row
            openai_client, api_client = init_new_conversation(use_api, request.bot_id)
            
            try:
                # Simulate conversation
                if use_api:
                    message_history, response_times, full_log = simulate_with_api(row, openai_client, api_client)
                else:
                    message_history, response_times = simulate_with_openai(row, openai_client)
                    full_log = [''] * len(message_history)
                
                # Prepare current row data
                current_messages = []
                initial_message_count = 0
                if not use_api and not pd.isna(row['initialConversationHistory']):
                    initial_message_count = len(json.loads(row['initialConversationHistory']))

                for i, msg in enumerate(message_history):
                    response_time = 0
                    if i >= initial_message_count:
                        response_idx = i - initial_message_count
                        response_time = response_times[response_idx] if response_idx < len(response_times) else 0
                    
                    current_full_log = full_log[i] if use_api and i < len(full_log) else ''
                    
                    current_messages.append({
                        'role': msg['role'],
                        'content': msg['content'],
                        'response_time': response_time,
                        'roleA_prompt': row['roleA_prompt'],
                        'roleB_prompt': row['roleB_prompt'] if not use_api else f"Using API (Bot ID: {request.bot_id})",
                        'useApiOrPrompt': row['useApiOrPrompt'],
                        'full_log': current_full_log
                    })
                
                processed_rows.extend(current_messages)
                
                # Export to Excel
                df_new = pd.DataFrame(current_messages, columns=[
                    'Role', 
                    'Content', 
                    'Response Time',
                    'RoleA Prompt',
                    'RoleB Prompt',
                    'useApiOrPrompt',
                    'Full Log'
                ])
                export_conversations_to_excel(df_new, output_path)
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error processing row {index + 1}: {str(e)}")

        # Thay vì trả về JSON response, trả về file Excel
        return FileResponse(
            path=output_path,
            filename=request.output_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
