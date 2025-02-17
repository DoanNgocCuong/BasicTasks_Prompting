import streamlit as st
import pandas as pd
import requests
import time
from pathlib import Path

API_URL = "http://localhost:8000"

st.set_page_config(page_title="CRUL Processor", layout="wide")

st.title("CRUL Command Processor")

# Sidebar for file upload and settings
with st.sidebar:
    st.header("Settings")
    
    # File upload
    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx'])
    
    if uploaded_file:
        # Upload file to API
        files = {'file': uploaded_file}
        response = requests.post(f"{API_URL}/upload", files=files)
        if response.status_code == 200:
            st.success("File uploaded successfully!")
            filename = response.json()['filename']
        else:
            st.error("Error uploading file")

    # Get list of available files
    response = requests.get(f"{API_URL}/files")
    if response.status_code == 200:
        files = response.json()['files']
        selected_file = st.selectbox("Select input file", files if files else ["No files available"])
    
    # Process settings
    output_file = st.text_input("Output filename", "output.xlsx")
    sheet_name = st.text_input("Sheet name", "Trang tính1")
    start_row = st.number_input("Start row", min_value=1, value=1)
    end_row = st.number_input("End row", min_value=start_row, value=None)
    
    if st.button("Process File"):
        if selected_file and selected_file != "No files available":
            # Start processing
            data = {
                "input_file": selected_file,
                "output_file": output_file,
                "sheet_name": sheet_name,
                "start_row": start_row,
                "end_row": end_row
            }
            response = requests.post(f"{API_URL}/process", json=data)
            if response.status_code == 202:
                st.success("Processing started!")
            else:
                st.error(f"Error starting process: {response.json().get('detail', '')}")

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.header("Processing Status")
    
    # Status display
    if st.button("Refresh Status"):
        response = requests.get(f"{API_URL}/status")
        if response.status_code == 200:
            status = response.json()
            st.write("**Status:**", status['status'])
            st.write("**Message:**", status['message'])
            if status['total_rows']:
                progress = (status['current_row'] or 0) / status['total_rows']
                st.progress(progress)
                st.write(f"Progress: {status['current_row']}/{status['total_rows']} rows")

with col2:
    st.header("Available Files")
    
    # Show available files with download buttons
    response = requests.get(f"{API_URL}/files")
    if response.status_code == 200:
        files = response.json()['files']
        for file in files:
            col1, col2 = st.columns([3,1])
            col1.write(file)
            if col2.button("Download", key=file):
                response = requests.get(f"{API_URL}/download/{file}")
                if response.status_code == 200:
                    st.download_button(
                        label="Click to download",
                        data=response.content,
                        file_name=file,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

    # Show preview of selected file
    if selected_file and selected_file != "No files available":
        st.subheader(f"Preview of {selected_file}")
        try:
            df = pd.read_excel(Path(__file__).parent / selected_file)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error loading preview: {str(e)}")
