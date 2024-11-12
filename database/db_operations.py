import pandas as pd
import pymysql
import streamlit as st
from constants import constants
from services import database_connection

# # MySQL connection settings
# DB_HOST = "localhost"
# DB_USER = "root"
# DB_PASSWORD = "root"
# DB_NAME = "python_training_management_database"

# # Test database connection
# def test_database_connection():
#     try:
#         connection = pymysql.connect(host=constants.DB_HOST, user=constants.DB_USER, password=constants.DB_PASSWORD, database=constants.DB_NAME)
#         connection.close()
#         return True
#     except pymysql.MySQLError as e:
#         print(f"Database connection failed: {e}")
#         return False

# # Establish a connection to MySQL
# def create_connection():
#     return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

def csv_to_dataframe():

    hiring_data = pd.read_csv('''data/hiring_data.csv''')
    training_data = pd.read_csv('''data/python_training_data.csv''')
    training_schedule_data= pd.read_csv('''data/training_schedule_data.csv''')
    
    # For Employee and Skills
    employees= hiring_data.iloc[:,:10]
    employee_skill= hiring_data.iloc[:,[0, -1]]

    # For Training data and training schedule
    python_training= training_data
    training_schedule= training_schedule_data

    return employees, employee_skill, python_training, training_schedule

# Process and insert CSV files based on file type
def clean_data():

    df= csv_to_dataframe()
    employees= df[0]
    employee_skill= df[1]
    python_training= df[2]
    training_schedule= df[3]

    clean_employees= employees.dropna(subset= ['Emp_ID'])

    clean_employees['Emp_ID'] = clean_employees['Emp_ID'].astype(int)
    clean_employees['Experience'] = clean_employees['Experience'].astype(int)
    clean_employees['Bench Duration'] = clean_employees['Bench Duration'].astype(int)

    clean_employee_skill= employee_skill.dropna(subset= ['Emp_ID'])
    clean_employee_skill['Emp_ID'] = clean_employee_skill['Emp_ID'].astype(int) 
    clean_employee_skill['Skills'] = clean_employee_skill['Skills'].str.split(', ')
    clean_employee_skill_exploded = clean_employee_skill.explode('Skills')
    clean_employee_skill_exploded.rename(columns={'Skills':'Skill_Name'}, inplace= True)

    # print(clean_employee_skill_exploded)

    clean_python_training= python_training.drop(python_training.columns[2:4],axis= 1)
    
    for column in clean_python_training.columns[1:7]:
    
        clean_python_training[f'{column}'] = clean_python_training[f'{column}'].astype(int)
    clean_python_training['Assessment_Date'] = pd.to_datetime(clean_python_training['Assessment_Date'])


    clean_training_schedule= training_schedule.dropna(subset= ['Team_ID'])
    for column in clean_training_schedule.columns[1:3]:
    
        clean_training_schedule[f'{column}'] = pd.to_datetime(clean_training_schedule[f'{column}'])
    clean_training_schedule['Duration'] = clean_training_schedule['Duration'].astype(int) 


    return clean_employees, clean_employee_skill_exploded, clean_python_training, clean_training_schedule

def data_upload(connection):
    df= clean_data()
    
    employees= df[0]
    employee_skill= df[1]
    python_training= df[2]
    training_schedule= df[3]

    for column in employees.columns:
        print(f'{column}:{type(employees[column].iloc[0])}')

    for index, row in employees.iterrows():
        sql_query = "INSERT INTO Employees VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = tuple(row)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()

    for index, row in python_training.iterrows():
        sql_query = "INSERT INTO Python_Training VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = tuple(row)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()

    query = "SELECT * FROM Skills"
    df_skills = pd.read_sql(query, connection)

    employee_skill_new= pd.merge(employee_skill,df_skills, on = ['Skill_Name'],how= 'inner')
    employee_skill_new= employee_skill_new.drop(employee_skill_new.columns[1],axis= 1)

    for index, row in employee_skill_new.iterrows():
        sql_query = "INSERT INTO Employee_Skills VALUES (%s, %s)"
        values = tuple(row)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()

    for index, row in training_schedule.iterrows():
        sql_query = "INSERT INTO Training_Schedule VALUES (%s, %s,%s, %s, %s)"
        values = tuple(row)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()


    connection.close()
 
    print("Data inserted successfully!")

# Fetch data from a specific MySQL table
def fetch_data_from_mysql(table_name):
    connection = database_connection.create_connection()
    try:
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql(query, connection)
    except Exception as e:
        st.error(f"Error fetching data from {table_name}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        connection.close()
