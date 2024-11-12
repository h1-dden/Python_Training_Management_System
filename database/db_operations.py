import pandas as pd
import pymysql
import streamlit as st

# MySQL connection settings
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "python_training_management_database"

# Test database connection
def test_database_connection():
    try:
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        connection.close()
        return True
    except pymysql.MySQLError as e:
        print(f"Database connection failed: {e}")
        return False

# Establish a connection to MySQL
def create_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

def insert_dataframe_to_mysql(df, table_name, connection):
    cursor = connection.cursor()

    column_mapping = {
        'Emp_ID': 'Emp_ID',
        'Emp_Name': 'Emp_Name',
        'Email_ID': 'Email_ID',
        'Experience': 'Experience',
        'Stack': 'Stack',
        'Grade': 'Grade',
        'Bench Status': 'Bench_Status',  
        'Bench Duration': 'Bench_Duration',
        'Deployment Status': 'Deployment_Status',
        'Communication Level': 'Communication_Level',
    }
    
    # Rename DataFrame columns to match MySQL table structure
    df = df.rename(columns=column_mapping)

    # Ensure only the necessary columns are in the DataFrame
    df = df[list(column_mapping.values())]

    columns = ', '.join([f"`{col}`" for col in df.columns])
    placeholders = ', '.join(['%s'] * len(df.columns))
    sql_query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
    
    # Insert each row from the DataFrame into the MySQL table
    for _, row in df.iterrows():
        values = tuple(row)
        cursor.execute(sql_query, values)
    connection.commit()
    cursor.close()
    st.sidebar.success(f"Data inserted successfully into {table_name}!")

# Process and insert CSV files based on file type
def process_and_insert_csv(uploaded_files):
    connection = create_connection()
    try:
        for file_type, file in uploaded_files.items():
            if file:
                df = pd.read_csv(file)
                insert_dataframe_to_mysql(df, file_type, connection)
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}")
    finally:
        connection.close()

# Fetch data from a specific MySQL table
def fetch_data_from_mysql(table_name):
    connection = create_connection()
    try:
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql(query, connection)
    except Exception as e:
        st.error(f"Error fetching data from {table_name}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        connection.close()
