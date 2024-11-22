import pandas as pd
from services import get_data
from database import db_operations


def clean_data():

    #Import data from get_data after the conversion of csv to Dataframe and unpack it
    df= get_data.csv_to_dataframe()
    employees= df[0]
    employee_skill= df[1]
    python_training= df[2]
    training_schedule= df[3]

    #Cleaning of employees dataframe
    clean_employees= employees.dropna(subset= ['Emp_ID'])
    clean_employees['Emp_ID'] = clean_employees['Emp_ID'].astype(int)
    clean_employees['Experience'] = clean_employees['Experience'].astype(int)
    clean_employees['Bench Duration'] = clean_employees['Bench Duration'].astype(int)

    #cleaning of employee_skill dataframe
    clean_employee_skill= employee_skill.dropna(subset= ['Emp_ID'])
    clean_employee_skill['Emp_ID'] = clean_employee_skill['Emp_ID'].astype(int)
    clean_employee_skill['Skills'] = clean_employee_skill['Skills'].str.split(', ')
    clean_employee_skill_exploded = clean_employee_skill.explode('Skills')
    clean_employee_skill_exploded.rename(columns={'Skills':'Skill_Name'}, inplace= True)

    #cleaning of python_training dataframe
    clean_python_training= python_training
    clean_python_training['Emp_ID'] = clean_python_training['Emp_ID'].astype(int)
    for column in clean_python_training.columns[3:8]:   
        clean_python_training[f'{column}'] = clean_python_training[f'{column}'].astype(int)
    clean_python_training['Assessment_Date'] = pd.to_datetime(clean_python_training['Assessment_Date'])

    #cleaning of training_schedule dataframe 
    clean_training_schedule= training_schedule.dropna(subset= ['Team_ID'])
    for column in clean_training_schedule.columns[1:3]:  
        clean_training_schedule[f'{column}'] = pd.to_datetime(clean_training_schedule[f'{column}'])
    clean_training_schedule['Duration'] = clean_training_schedule['Duration'].astype(int)
 
 
    return clean_employees, clean_employee_skill_exploded, clean_python_training, clean_training_schedule

def create_test_scores_dataframe():

    """Fetch data and create a DataFrame with test scores for each unique employee."""

    # Fetch data from the database
    training_data_df = db_operations.fetch_training_data()

    # Pivot the DataFrame

    test_scores_df = training_data_df.pivot_table(
        index=['Team_ID', 'Emp_Name','Email_ID'],  # Rows are based on team_ID and emp_ID
        columns='Test_Name',         # Each unique test name becomes a column
        values='Test_Score',         # Values are from test_score
        aggfunc='first'              # Handle duplicate combinations (if any)
    ).reset_index()
    test_scores_df.index = range(1, len(test_scores_df) + 1)

    #create avg test scores
    test_scores_df['Avg_Score'] = test_scores_df.iloc[:, 3:].mean(axis=1)

    #Fill NaN values (if any) with 0
    #test_scores_df = test_scores_df.fillna(0)
    return test_scores_df
