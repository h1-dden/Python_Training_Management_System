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
   
    def upload_employees():
        # for entry in table Employees
        emp_ids = employees['Emp_ID'].tolist()
 
        # Check if any of the Emp_IDs already exists in the database
        check_query = "SELECT Emp_ID FROM Employees WHERE Emp_ID IN %s"
        with connection.cursor() as cursor:
            cursor.execute(check_query, (tuple(emp_ids),))
            existing_ids = set(row[0] for row in cursor.fetchall())
 
        # Determine if there are any new Emp_IDs
        new_rows = employees[~employees['Emp_ID'].isin(existing_ids)]
 
        if new_rows.empty:
            print("Data already exists for all Emp_IDs in the DataFrame.")
        else:
            # Insert new rows into the database
            sql_query = "INSERT INTO Employees VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            with connection.cursor() as cursor:
                for index, row in new_rows.iterrows():
                    values = tuple(row)
                    cursor.execute(sql_query, values)
                connection.commit()
 
    def upload_python_training():
        # Collect Emp_ID and Assessment_Date pairs from the DataFrame
        emp_assessment_pairs = list(zip(python_training.iloc[:, 1], python_training.iloc[:, -2]))
 
        # Check if any of the Emp_ID and Assessment_Date pairs already exists in the database
        check_query = """
            SELECT Emp_ID, Assessment_Date FROM Python_Training
            WHERE (Emp_ID, Assessment_Date) IN %s
        """
        with connection.cursor() as cursor:
            cursor.execute(check_query, (tuple(emp_assessment_pairs),))
            existing_pairs = set(cursor.fetchall())  # Fetch all existing pairs
 
        # Determine if there are any new pairs
        new_rows = python_training[
            ~python_training.apply(lambda row: (row[1], row[-2]) in existing_pairs, axis=1)
        ]
 
        if new_rows.empty:
            print("Data already exists for all Emp_ID and Assessment_Date combinations in the DataFrame.")
        else:
            # Insert new rows into the database
            sql_query = "INSERT INTO Python_Training VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            with connection.cursor() as cursor:
                for index, row in new_rows.iterrows():
                    values = tuple(row)
                    cursor.execute(sql_query, values)
                connection.commit()
 
    def upload_employee_skills():
        query = "SELECT * FROM Skills"
        df_skills = pd.read_sql(query, connection)
 
        employee_skill_new= pd.merge(employee_skill,df_skills, on = ['Skill_Name'],how= 'inner')
        employee_skill_new= employee_skill_new.drop(employee_skill_new.columns[1],axis= 1)
 
        # Collect Emp_ID and Skill_ID pairs from the DataFrame
        emp_skill_pairs = list(zip(employee_skill_new.iloc[:, 0], employee_skill_new.iloc[:, 1]))
 
        # Check if any of the Emp_ID and skills pairs already exists in the database
        check_query = """
            SELECT Emp_ID, Skill_ID FROM Employee_Skills
            WHERE (Emp_ID, Skill_ID) IN %s
        """
        with connection.cursor() as cursor:
            cursor.execute(check_query, (tuple(emp_skill_pairs),))
            existing_pairs = set(cursor.fetchall())  # Fetch all existing pairs
 
        # Determine if there are any new pairs
        new_rows = employee_skill_new[
            ~employee_skill_new.apply(lambda row: (row[0], row[1]) in existing_pairs, axis=1)
        ]
 
        if new_rows.empty:
            print("Data already exists for all Emp_ID and Skill_ID combinations in the CSV.")
        else:
            # Insert new rows into the database
            sql_query = "INSERT INTO Employee_Skills VALUES (%s, %s)"
            with connection.cursor() as cursor:
                for index, row in new_rows.iterrows():
                    values = tuple(row)
                    cursor.execute(sql_query, values)
                connection.commit()
 
    def upload_training_schedule():
        # for entry in table training_schedule
        team_ids = training_schedule['Team_ID'].tolist()
 
        # # Assuming the second to last column is the Assessment_Date
        # start_date_col_index = 1
        # last_day_col_index= 2
       
        # # Convert the Assessment_Date column to the correct format
        # training_schedule.iloc[:, start_date_col_index] = pd.to_datetime(
        #     training_schedule.iloc[:, start_date_col_index],
        #     format='%d-%m-%Y',  # Specify the current format
        #     errors='coerce'     # Coerce errors to NaT (Not a Time)
        # ).dt.strftime('%m-%d-%Y')  # Convert to the required format
 
        # training_schedule.iloc[:, last_day_col_index] = pd.to_datetime(
        #     training_schedule.iloc[:, last_day_col_index],
        #     format='%d-%m-%Y',  # Specify the current format
        #     errors='coerce'     # Coerce errors to NaT (Not a Time)
        # ).dt.strftime('%m-%d-%Y')  # Convert to the required format
 
        # Check if any of the Emp_IDs already exists in the database
        check_query = "SELECT Team_ID FROM Training_Schedule WHERE Team_ID IN %s"
        with connection.cursor() as cursor:
            cursor.execute(check_query, (tuple(team_ids),))
            existing_ids = set(row[0] for row in cursor.fetchall())
 
        # Determine if there are any new Emp_IDs
        new_rows = training_schedule[~training_schedule['Team_ID'].isin(existing_ids)]
 
        if new_rows.empty:
            print("Data already exists for all Team_IDs in the DataFrame.")
        else:
            # Insert new rows into the database
            sql_query = "INSERT INTO Training_Schedule VALUES (%s, %s ,%s, %s, %s, %s)"
            with connection.cursor() as cursor:
                for index, row in new_rows.iterrows():
                    values = tuple(row)
                    cursor.execute(sql_query, values)
                connection.commit()
   
    upload_employees()
    upload_employee_skills()
    upload_python_training()
    upload_training_schedule()

 
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


import pandas as pd

def fetch_employee_data(connection):
    """Fetch employee data from the database."""
    query = "SELECT * FROM Employees"
    return pd.read_sql(query, connection)

def fetch_training_data(connection):
    """Fetch training data from the database."""
    query = "SELECT * FROM python_training"
    return pd.read_sql(query, connection)

def fetch_training_schedule_data(connection):
    """Fetch training schedule data from the database."""
    query = "SELECT * FROM Training_Schedule"
    return pd.read_sql(query, connection)
