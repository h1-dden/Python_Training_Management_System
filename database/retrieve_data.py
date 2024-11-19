
import pandas as pd
from services import database_connection

def fetch_data(query):

    """Fetch data from MySQL database."""

    connection = database_connection.create_connection() 
    df = pd.read_sql(query, connection)
    connection.close()
    return df