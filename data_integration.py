import pandas as pd
from database.db_operations import create_connection

def get_data():
    # Load CSV data
    hiring_data = pd.read_csv('data/hiring_data.csv')
    training_data = pd.read_csv('data/training_data.csv')
    training_schedule_data = pd.read_csv('data/training_schedule_data.csv')
   
    # Extracting relevant parts for different tables
    employees = hiring_data.iloc[:, :10]
    employee_skill = hiring_data.iloc[:, [0, -1]]
    python_training = training_data
    training_schedule = training_schedule_data

    return employees, employee_skill, python_training, training_schedule

def clean_data():
    # Get raw data
    employees, employee_skill, python_training, training_schedule = get_data()
   
    # Clean Employees data
    clean_employees = employees.dropna(subset=['Emp_ID'])
    clean_employees['Emp_ID'] = clean_employees['Emp_ID'].astype(int)
    clean_employees['Experience'] = clean_employees['Experience'].astype(int)
    clean_employees['Bench Duration'] = clean_employees['Bench Duration'].astype(int)
   
    # Clean other tables by dropping rows with missing key identifiers
    clean_employee_skill = employee_skill.dropna(subset=['Emp_ID'])
    clean_python_training = python_training.dropna(subset=['Team_ID'])
    clean_training_schedule = training_schedule.dropna(subset=['Team_ID'])

    return clean_employees, clean_employee_skill, clean_python_training, clean_training_schedule

def data_upload():
    # Clean and prepare data for upload
    clean_employees, clean_employee_skill, clean_python_training, clean_training_schedule = clean_data()
    connection = create_connection()
    
    # Upload Employees data
    for _, row in clean_employees.iterrows():
        sql_query = "INSERT INTO Employees VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = tuple(row)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()

    # Upload Employee Skills data
    for _, row in clean_employee_skill.iterrows():
        sql_query = "INSERT INTO Employee_Skills VALUES (%s, %s)"
        values = tuple(row)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()

    # Upload Python Training data
    for _, row in clean_python_training.iterrows():
        sql_query = "INSERT INTO Python_Training VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = tuple(row)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()

    # Upload Training Schedule data
    for _, row in clean_training_schedule.iterrows():
        sql_query = "INSERT INTO Training_Schedule VALUES (%s, %s, %s, %s, %s)"
        values = tuple(row)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            connection.commit()
    
    connection.close()
    print("Data inserted successfully!")

# Run data upload function
data_upload()
