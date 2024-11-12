import pandas as pd
import pymysql

# Connect to MySQL database
connection = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "python_training_management_database"
)


# Read Excel file
df = pd.read_csv(r"utils\database scripts\teamdata.csv")

# Insert DataFrame into MySQL table
for index, row in df.iterrows():
    sql_query = "INSERT INTO Training_data VALUES (%s, %s)"
    values = tuple(row)
    with connection.cursor() as cursor:
        cursor.execute(sql_query, values)
        connection.commit()

connection.close()

print("Data inserted successfully!")