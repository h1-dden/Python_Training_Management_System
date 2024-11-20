
import streamlit as st
import os
from view import template_creation
from database import db_operations
from utils import save_file
from services import upload_data

def show_admin_client(connection,data_path):

    """ Show admin client page with template creation and file upload functionality"""

    st.sidebar.header("Admin Menu")
    st.sidebar.header(" ")
    st.sidebar.subheader("Data Management")

    template_dir = "templates"
    templates = {
        "Training Schedule": os.path.join(template_dir, "training_schedule_data_template.csv"),
        "Employees": os.path.join(template_dir, "hiring_template.csv"),
        "Python Training": os.path.join(template_dir, "training_data_template.csv")
    }
    template_creation.download_all_templates() #download templates
    
    # File upload and save functionality for Hiring Data
    st.sidebar.header(" ")
    st.sidebar.subheader("Employee Data (Hiring Data)")
    hiring_data_file = st.sidebar.file_uploader("Upload Hiring Data CSV", type="csv", key="hiring_data")
    
    if hiring_data_file:
        if st.sidebar.button("Upload Hiring Data"):
            hiring_data_path = os.path.join(data_path, "hiring_data.csv")
            save_file.save_uploaded_file(hiring_data_file, hiring_data_path)
    
    # File upload and save functionality for Training Schedule Data
    st.sidebar.subheader("Training Schedule Data")
    training_schedule_data_file = st.sidebar.file_uploader("Upload Training Schedule Data CSV", type="csv", key="training_schedule_data")
    
    if training_schedule_data_file:
        if st.sidebar.button("Upload Training Schedule Data"):
            training_schedule_data_path = os.path.join(data_path, "training_schedule_data.csv")
            save_file.save_uploaded_file(training_schedule_data_file, training_schedule_data_path)
    
    # File upload and save functionality for Python Training Data
    st.sidebar.subheader("Python Training Data")
    python_training_data_file = st.sidebar.file_uploader("Upload Python Training Data CSV", type="csv", key="python_training_data")
    
    if python_training_data_file:
        if st.sidebar.button("Upload Python Training Data"):
            python_training_data_path = os.path.join(data_path, "python_training_data.csv")
            save_file.save_uploaded_file(python_training_data_file, python_training_data_path)
   
    # Save data to database
    if st.sidebar.button("Save Data"):
        try:
            upload_data.data_upload(connection)
            st.sidebar.success("Data saved successfully!")
        except Exception as e:
            st.sidebar.error(f"Error occurred during data saving: {e}")
