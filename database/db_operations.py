
import pandas as pd
from database import retrieve_data

def fetch_employee_data():

    """Fetch employee data from the database."""

    query = "SELECT * FROM Employees"
    employee_data = retrieve_data.fetch_data(query)
    return employee_data

def fetch_training_data():

    """Fetch training data from the database."""

    query = (
        "Select e.Emp_Name,e.Email_ID,p.* from Employees e right join Python_Training p "
        "on e.Emp_ID=p.Emp_ID"
        )
    query_df = employee_data = retrieve_data.fetch_data(query)
    query_df.index = range(1, len(query_df) + 1) #indexing starts from 1 and not 0
    return query_df

def fetch_training_schedule_data():

    """Fetch training schedule data from the database."""

    query = "SELECT * FROM Training_Schedule"
    training_schedule_data = retrieve_data.fetch_data(query)
    return training_schedule_data
