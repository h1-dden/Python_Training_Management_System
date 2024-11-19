import streamlit as st
import zipfile
import os
import io

def download_template(template_file, description):

    """Function to download CSV templates """

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