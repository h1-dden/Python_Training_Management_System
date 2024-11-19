import pandas as pd

# Process data from a CSV file based on the table type
def process_data(file, table_type):
    df = pd.read_csv(file)
    
    # You can add data validation or transformation here based on table_type
    if table_type == "Employees":
        required_columns = ["Emp_ID", "Emp_Name", "Email_ID", "Experience", "Stack", "Grade", "Bench_Status", "Bench_Duration", "Deployment_Status", "Communication_Level"]
        df = df[required_columns]
    elif table_type == "Skills":
        required_columns = ["Skill_ID", "Skill_Name"]
        df = df[required_columns]
    elif table_type == "Python_Training":
        required_columns = ["Team_ID", "Emp_ID", "Test_Score", "Presentation", "Project_Assignment", "Overall_Rating", "Overall_Feedback", "Assessment_Date"]
        df = df[required_columns]
        df["Assessment_Date"] = pd.to_datetime(df["Assessment_Date"], errors="coerce")

    return df
