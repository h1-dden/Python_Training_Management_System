import pymysql
from constants import constants

def test_database_connection():
    try:
        connection = pymysql.connect(host=constants.DB_HOST, user=constants.DB_USER, password=constants.DB_PASSWORD, database=constants.DB_NAME)
        return True
    except pymysql.MySQLError as e:
        print(f"Database connection failed: {e}")
        return False

def create_connection():
    return pymysql.connect(host=constants.DB_HOST, user=constants.DB_USER, password=constants.DB_PASSWORD, database=constants.DB_NAME)