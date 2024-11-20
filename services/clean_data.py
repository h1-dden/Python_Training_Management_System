import pandas as pd
from services import get_data

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
    for column in clean_python_training.columns[1:7]:   
        clean_python_training[f'{column}'] = clean_python_training[f'{column}'].astype(int)
    clean_python_training['Assessment_Date'] = pd.to_datetime(clean_python_training['Assessment_Date'])

    #cleaning of training_schedule dataframe 
    clean_training_schedule= training_schedule.dropna(subset= ['Team_ID'])
    for column in clean_training_schedule.columns[1:3]:  
        clean_training_schedule[f'{column}'] = pd.to_datetime(clean_training_schedule[f'{column}'])
    clean_training_schedule['Duration'] = clean_training_schedule['Duration'].astype(int)
 
 
    return clean_employees, clean_employee_skill_exploded, clean_python_training, clean_training_schedule
