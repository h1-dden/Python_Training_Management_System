'''
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
 '''

import streamlit as st
import bcrypt
import os
import zipfile
import io
import pandas as pd
from utils import visualization
from database import db_operations
from services import database_connection

# Set up Streamlit page
st.set_page_config(page_title="Yash Technologies Management System", page_icon="📊", layout="wide")

# Establish database connection
connection = database_connection.create_connection()

# Define user credentials for login
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

# Initialize session state for login, role, and page
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.page = "Dashboard"
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'password' not in st.session_state:
    st.session_state.password = ""

# Authenticate user function
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

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.page = "Dashboard"
    st.rerun()


# Function to download CSV templates
def download_template(template_file, description):
    with open(template_file, "r") as file:
        st.download_button(
            label=f"Download {description} Template",
            data=file.read(),
            file_name=os.path.basename(template_file),
            mime="text/csv"
        )

# Function to download all templates in a ZIP
def download_all_templates():
    template_dir = "templates"
    templates = {
        "Training Schedule": os.path.join(template_dir, "training_schedule_data_template.csv"),
        "Employees": os.path.join(template_dir, "hiring_data_template.csv"),
        "Python Training": os.path.join(template_dir, "training_data_template.csv")
    }
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for template_name, template_path in templates.items():
            zip_file.write(template_path, arcname=f"{template_name}_template.csv")
    zip_buffer.seek(0)
    st.sidebar.download_button(
        label="Download All Templates (ZIP)",
        data=zip_buffer,
        file_name="CSV_Templates.zip",
        mime="application/zip"
    )

# Ensure data folder exists
data_folder = "data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Function to save uploaded file, replacing if it exists
def save_uploaded_file(uploaded_file, file_path):
    if os.path.exists(file_path):
        os.remove(file_path)  # Delete the old file if it exists
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"{os.path.basename(file_path)} saved successfully!")

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
    # Sidebar for navigation and logout
    st.sidebar.write(f"Logged in as: **{st.session_state.role.capitalize()}**")
    if st.sidebar.button("Logout"):
        logout()

    # Sidebar navigation
    st.sidebar.header("Navigation")
    if st.sidebar.button("Dashboard"):
        st.session_state.page = "Dashboard"
    if st.sidebar.button("Training Statistics"):
        st.session_state.page = "Training Statistics"

    # Admin-specific file upload and download section
    if st.session_state.role == 'admin':
        st.sidebar.header("Admin Menu")
        st.sidebar.header("Data Management")
        st.sidebar.markdown("Admins can upload CSV files and download templates.")

        # Individual CSV template download buttons
        template_dir = "templates"
        templates = {
            "Training Schedule": os.path.join(template_dir, "training_schedule_data_template.csv"),
            "Employees": os.path.join(template_dir, "hiring_template.csv"),
            "Python Training": os.path.join(template_dir, "training_data_template.csv")
        }
        download_all_templates()

        # File upload and save functionality for Hiring Data
        st.sidebar.subheader("Employee Data (Hiring Data)")
        hiring_data_file = st.sidebar.file_uploader("Upload Hiring Data CSV", type="csv", key="hiring_data")
        if hiring_data_file:
            if st.sidebar.button("Upload Hiring Data"):
                hiring_data_path = os.path.join(data_folder, "hiring_data.csv")
                save_uploaded_file(hiring_data_file, hiring_data_path)

        # File upload and save functionality for Training Schedule Data
        st.sidebar.subheader("Training Schedule Data")
        training_schedule_data_file = st.sidebar.file_uploader("Upload Training Schedule Data CSV", type="csv", key="training_schedule_data")
        if training_schedule_data_file:
            if st.sidebar.button("Upload Training Schedule Data"):
                training_schedule_data_path = os.path.join(data_folder, "training_schedule_data.csv")
                save_uploaded_file(training_schedule_data_file, training_schedule_data_path)

        # File upload and save functionality for Python Training Data
        st.sidebar.subheader("Python Training Data")
        python_training_data_file = st.sidebar.file_uploader("Upload Python Training Data CSV", type="csv", key="python_training_data")
        if python_training_data_file:
            if st.sidebar.button("Upload Python Training Data"):
                python_training_data_path = os.path.join(data_folder, "python_training_data.csv")
                save_uploaded_file(python_training_data_file, python_training_data_path)

        # Save data to database
        if st.sidebar.button("Save Data"):
            try:
                db_operations.data_upload(connection)
                st.sidebar.success("Data saved successfully!")
            except Exception as e:
                st.sidebar.error(f"Error occurred during data saving: {e}")

    # Display content based on page selection
    if st.session_state.page == "Dashboard":
        st.header("Employee and Training Insights - Dashboard")
        visualization.show_general_visualizations()  # General employee statistics visualizations

        # Display Employee Table with Filters
        st.subheader("Employee Table with Filters")
        employee_df = db_operations.fetch_employee_data(connection)  # Fetch data from database
        with st.expander("Filter Employee Data"):
            grade_filter = st.multiselect("Filter by Grade", options=employee_df['Grade'].unique())
            comm_level_filter = st.multiselect("Filter by Communication Level", options=employee_df['Communication_Level'].unique())
            deployment_filter = st.multiselect("Filter by Deployment Status", options=employee_df['Deployment_Status'].unique())
            experinece_filter = st.multiselect("Filter by Experience", options=employee_df['Experience'].unique())
        # Apply filters
        if grade_filter:
            employee_df = employee_df[employee_df['Grade'].isin(grade_filter)]
        if comm_level_filter:
            employee_df = employee_df[employee_df['Communication_Level'].isin(comm_level_filter)]
        if deployment_filter:
            employee_df = employee_df[employee_df['Deployment_Status'].isin(deployment_filter)]
        if experinece_filter:
            employee_df = employee_df[employee_df['Experience'].isin(experinece_filter) ]     
        # Display filtered employee table
        st.dataframe(employee_df, use_container_width=True)
        
        # Download filtered data
        csv = employee_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Filtered Employee Data", data=csv, file_name="filtered_employee_data.csv", mime="text/csv")

        # Filtered Data Visualization
        st.subheader("Filtered Employee Data Visualization")
        visualization.visualize_filtered_employee_data(employee_df)

    elif st.session_state.page == "Training Statistics":
        st.header("Training Data Statistics")

        # Display Training Table with Filters
        training_df = db_operations.fetch_training_data(connection)  # Fetch training data from database
        with st.expander("Filter Training Data"):
            team_filter = st.multiselect("Filter by Team", options=training_df['Team_ID'].unique())
            score_filter = st.slider("Filter by Minimum Test Score", min_value=int(training_df['Test_Score'].min()), max_value=int(training_df['Test_Score'].max()))
        
        # Apply filters
        if team_filter:
            training_df = training_df[training_df['Team_ID'].isin(team_filter)]
        training_df = training_df[training_df['Test_Score'] >= score_filter]
        
        # Display filtered training table
        st.dataframe(training_df, use_container_width=True)
        
        # Download filtered data
        csv_training = training_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Filtered Training Data", data=csv_training, file_name="filtered_training_data.csv", mime="text/csv")

        # Filtered Data Visualization
        st.subheader("Filtered Training Data Visualization")
        visualization.visualize_filtered_training_data(training_df)
