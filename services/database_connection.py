import pymysql
from constants import constants

connection = None

def create_connection():

    try:
        connection = pymysql.connect(host=constants.HOST ,user=constants.USER ,password=constants.PASSWORD , db=constants.DB_NAME)
        return connection
    
    except pymysql.MySQLError as e:
        print(f"Database connection failed: {e}")
        return False
       