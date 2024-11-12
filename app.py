import os
import streamlit as st
import bcrypt  
from database import db_operations
from utils import visualization

st.set_page_config(page_title="Yash Technologies Management System", page_icon="📊", layout="wide")

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

# Authentication
def authenticate(username, password):
    user = USER_CREDENTIALS.get(username)
    if user and bcrypt.checkpw(password.encode(), user['password']):
        st.session_state.logged_in = True
        st.session_state.role = user['role']
        st.session_state.username = ""  # Clear the username field
        st.session_state.password = ""  # Clear the password field
        st.rerun()  # Rerun the app to update UI
    else:
        st.error("Invalid username or password.")

# Logout function to reset session state
def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()  # Rerun the app to update UI

# Function to download CSV template
def download_template(template_file, description):
    with open(template_file, "r") as file:
        st.download_button(
            label=f"Download {description} Template",
            data=file.read(),
            file_name=os.path.basename(template_file),
            mime="text/csv"
        )

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

# Role-based Access
if st.session_state.logged_in:
    if st.session_state.role == 'admin':
        st.sidebar.header("Admin Menu")
        
        st.sidebar.header("Data Management Section")
        st.sidebar.markdown("You can upload CSV files and download format templates.")

        # CSV templates directory
        template_dir = "templates"
        templates = {
            "Training Schedule": os.path.join(template_dir, "training_schedule_data_template.csv"),
            "Employees": os.path.join(template_dir, "hiring_data_template.csv"),
            "Python Training": os.path.join(template_dir, "training_data_template.csv")
        }

        # File upload interface with template download buttons
        uploaded_files = {}
        for key, template_file in templates.items():
            st.sidebar.subheader(f"{key} Data")
            download_template(template_file, key)  
            uploaded_files[key] = st.sidebar.file_uploader(f"Upload {key} Data CSV", type="csv")

        if st.sidebar.button("Process and Save Data"):
            try:
                db_operations.process_and_insert_csv(uploaded_files)
                st.sidebar.success("Data processed and saved successfully!")
            except Exception as e:
                st.sidebar.error(f"An error occurred while uploading data: {e}")
    
    st.header("Employee and Training Insights")
    visualization.show_visualizations() 
else:
    st.info("Please log in to access the application.")
