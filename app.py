import streamlit as st
import bcrypt  
import os
import zipfile
import io
from utils import visualization
from database import db_operations
from services import database_connection
 
st.set_page_config(page_title="Yash Technologies Management System", page_icon="📊", layout="wide")
 
connection=database_connection.create_connection()

USER_CREDENTIALS = {
    'admin': {
        'password': bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()),
        'role': 'admin'
    },
    'user': {
        'password': bcrypt.hashpw("user123".encode(), bcrypt.gensalt()),
        'role': 'user'
    }
}
 
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'password' not in st.session_state:
    st.session_state.password = ""
 
 
def authenticate(username, password):
    user = USER_CREDENTIALS.get(username)
    if user and bcrypt.checkpw(password.encode(), user['password']):
        st.session_state.logged_in = True
        st.session_state.role = user['role']
        st.session_state.username = ""
        st.session_state.password = ""
        st.rerun()
    else:
        st.error("Invalid username or password.")
 
def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()  
 
# Function to download CSV template
def download_template(template_file, description):
    with open(template_file, "r") as file:
        st.download_button(
            label=f"Download {description} Template",
            data=file.read(),
            file_name=os.path.basename(template_file),
            mime="text/csv"
        )
 
# Function to create and download a ZIP file containing all CSV templates
def download_all_templates():
    template_dir = "templates"
    templates = {
        "Training Schedule": os.path.join(template_dir, "training_schedule_data_template.csv"),
        "Employees": os.path.join(template_dir, "hiring_data_template.csv"),
        "Python Training": os.path.join(template_dir, "training_data_template.csv")
    }
 
    # Create an in-memory ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for template_name, template_path in templates.items():
            zip_file.write(template_path, arcname=f"{template_name}_template.csv")
 
    zip_buffer.seek(0)  # Rewind the buffer to the beginning
 
    # Download button for the ZIP file
    st.sidebar.download_button(
        label="Download All Templates (ZIP)",
        data=zip_buffer,
        file_name="CSV_Templates.zip",
        mime="application/zip"
    )
 
# Ensure the `data` folder exists
data_folder = "data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
 
# Main app layout
st.image("images/download.png", width=135)
st.title("Yash Technologies Employee Management System")
 
# Login Section
if not st.session_state.logged_in:
    st.subheader("Login")
    st.session_state.username = st.text_input("Username", value=st.session_state.username)
    st.session_state.password = st.text_input("Password", type="password", value=st.session_state.password)
    login_button = st.button("Login")
 
    if login_button:
        authenticate(st.session_state.username, st.session_state.password)
else:
    st.sidebar.write(f"Logged in as: **{st.session_state.role.capitalize()}**")
    if st.sidebar.button("Logout"):
        logout()
 
# Role-based Content
if st.session_state.logged_in:
    if st.session_state.role == 'admin':
        st.sidebar.header("Admin Menu")
       
        # File upload section with download template buttons
        st.sidebar.header("Data Management")
        st.sidebar.markdown("Admins can upload CSV files and download templates.")
 
        # Individual CSV template download buttons
        template_dir = "templates"
        templates = {
            "Training Schedule": os.path.join(template_dir, "training_schedule_data_template.csv"),
            "Employees": os.path.join(template_dir, "hiring_template.csv"),
            "Python Training": os.path.join(template_dir, "training_data_template.csv")
        }
 
        # Download all templates as a single ZIP file
        download_all_templates()
 
        # File upload and saving for hiring data
        st.sidebar.subheader("Employee Data (Hiring Data)")
        hiring_data_file = st.sidebar.file_uploader("Upload Hiring Data CSV", type="csv")
        if hiring_data_file:
            hiring_data_path = os.path.join(data_folder, "hiring_data.csv")
            with open(hiring_data_path, "wb") as f:
                f.write(hiring_data_file.getbuffer())
            st.sidebar.success("Hiring data saved successfully!")
 
        # File upload and saving for training schedule data
        st.sidebar.subheader("Training Schedule Data")
        training_schedule_data_file = st.sidebar.file_uploader("Upload Training Schedule Data CSV", type="csv")
        if training_schedule_data_file:
            training_schedule_data_path = os.path.join(data_folder, "training_schedule_data.csv")
            with open(training_schedule_data_path, "wb") as f:
                f.write(training_schedule_data_file.getbuffer())
            st.sidebar.success("Training schedule data saved successfully!")
 
        # File upload and saving for python training data
        st.sidebar.subheader("Python Training Data")
        python_training_data_file = st.sidebar.file_uploader("Upload Python Training Data CSV", type="csv")
        if python_training_data_file:
            python_training_data_path = os.path.join(data_folder, "python_training_data.csv")
            with open(python_training_data_path, "wb") as f:
                f.write(python_training_data_file.getbuffer())
            st.sidebar.success("Python training data saved successfully!")

        if st.sidebar.button("Save Data"):
            try:
                db_operations.data_upload(connection)
                st.sidebar.success("Data saved successfully!!")
            except Exception as e:
                st.sidebar.error(f"Error Occured During Saving Data: {e}")

    st.header("Employee and Training Insights")
    visualization.show_visualizations()  
else:
    st.info("Please log in to access the application.")