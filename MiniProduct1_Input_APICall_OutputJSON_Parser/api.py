from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from pydantic import BaseModel
import pandas as pd
from pathlib import Path
from typing import Optional
import uvicorn
from main import execute_curl, is_json, process_row
import json
import shutil
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CRUL Processor API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CRULRequest(BaseModel):
    input_file: str
    output_file: str = "output.xlsx"  # Default output filename
    sheet_name: str = "Trang tính1"
    start_row: int = 1
    end_row: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "input_file": "input.xlsx",
                "output_file": "output.xlsx",
                "sheet_name": "Trang tính1",
                "start_row": 1,
                "end_row": 10
            }
        }

class ProcessStatus(BaseModel):
    status: str
    message: str
    current_row: Optional[int] = None
    total_rows: Optional[int] = None

# Store processing status
process_status = ProcessStatus(status="idle", message="No process running")

def process_excel_file(input_file: str, output_file: str, sheet_name: str, start_row: int, end_row: Optional[int] = None):
    try:
        # Define the base paths
        SCRIPTS_FOLDER = Path(__file__).parent
        INPUT_FILE = SCRIPTS_FOLDER / input_file
        OUTPUT_FILE = SCRIPTS_FOLDER / output_file

        # Read input Excel file
        df_input = pd.read_excel(INPUT_FILE, sheet_name=sheet_name)
        
        if df_input.empty:
            raise ValueError("Input file is empty")

        # Verify required column exists
        if 'CRUL' not in df_input.columns:
            raise ValueError("Missing required column 'CRUL'")

        # Convert 1-based to 0-based indexing and validate row ranges
        start_idx = start_row - 1
        end_idx = (end_row - 1) if end_row is not None else len(df_input) - 1

        # Validate start_row
        if start_idx < 0:
            raise ValueError(f"Start row {start_row} must be greater than 0")
        if start_idx >= len(df_input):
            raise ValueError(f"Start row {start_row} exceeds the number of rows in file ({len(df_input)})")

        # Validate end_row
        if end_idx >= len(df_input):
            # Automatically adjust end_idx to last row if it exceeds
            end_idx = len(df_input) - 1
            print(f"Warning: End row adjusted to {end_idx + 1} (last row in file)")
        if end_idx < start_idx:
            raise ValueError(f"End row {end_row} must be greater than or equal to start row {start_row}")

        # Create output DataFrame by copying input
        df_output = df_input.copy()

        # Update status
        global process_status
        process_status.status = "processing"
        process_status.total_rows = end_idx - start_idx + 1

        # Process specified rows and update immediately
        for index in range(start_idx, end_idx + 1):
            process_status.current_row = index + 1
            process_status.message = f"Processing row {index + 1} of {end_idx + 1}"

            CRUL_command = df_input.iloc[index]['CRUL']
            output, parsed_output = process_row(CRUL_command)

            if is_json(output):
                try:
                    json_data = json.loads(output)
                    if isinstance(json_data, dict):
                        # Store the raw response output
                        df_output.loc[index, 'Raw_Output'] = output
                        # Add JSON columns
                        for key, value in json_data.items():
                            col_name = f'JSON_{key}'
                            df_output.loc[index, col_name] = str(value)
                except Exception as e:
                    process_status.message = f"Error parsing JSON at row {index + 1}: {str(e)}"
            else:
                df_output.loc[index, 'Raw_Output'] = output

            # Save after each row
            df_output.to_excel(OUTPUT_FILE, index=False)

        process_status.status = "completed"
        process_status.message = "Processing completed successfully!"

    except Exception as e:
        process_status.status = "error"
        process_status.message = str(e)
        raise

@app.post("/process")
async def process_file(request: CRULRequest, background_tasks: BackgroundTasks):
    """
    Start processing an Excel file containing CRUL commands
    """
    try:
        # Verify file exists and is readable
        input_path = Path(__file__).parent / request.input_file
        if not input_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Input file '{request.input_file}' not found in {input_path}"
            )
        if not input_path.is_file():
            raise HTTPException(
                status_code=400,
                detail=f"'{request.input_file}' is not a file"
            )
            
        # Verify file can be opened as Excel
        try:
            pd.read_excel(input_path, sheet_name=request.sheet_name)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error reading Excel file: {str(e)}"
            )

        background_tasks.add_task(
            process_excel_file,
            request.input_file,
            request.output_file,
            request.sheet_name,
            request.start_row,
            request.end_row
        )
        return JSONResponse(
            content={
                "message": "Processing started",
                "status": "started"
            },
            status_code=202
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/status")
async def get_status():
    """
    Get current processing status
    """
    return process_status

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload an Excel file
    """
    try:
        # Save the uploaded file
        file_path = Path(__file__).parent / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return JSONResponse(
            content={
                "message": f"File {file.filename} uploaded successfully",
                "filename": file.filename
            },
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download an Excel file
    """
    try:
        file_path = Path(__file__).parent / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
            
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/files")
async def list_files():
    """
    List all Excel files in the directory
    """
    try:
        files = list(Path(__file__).parent.glob("*.xlsx"))
        return {
            "files": [file.name for file in files]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
