import os
import streamlit as st

# Function to save uploaded file, replacing if it exists
def save_uploaded_file(uploaded_file, file_path):
    if os.path.exists(file_path):
        os.remove(file_path)  # Delete the old file if it exists
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"{os.path.basename(file_path)} saved successfully!")