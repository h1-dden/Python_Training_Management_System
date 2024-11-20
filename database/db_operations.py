import pandas as pd
import streamlit as st
from services import database_connection

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
