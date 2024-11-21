import pandas as pd
import pymysql
from services import clean_data

def data_upload(connection):
    df= clean_data.clean_data()
   
    employees= df[0]
    employee_skill= df[1]
    python_training= df[2]
    training_schedule= df[3]


   
    def upload_employees():
        #Stack Separation
        query = "SELECT * FROM Skills"
        df_skills = pd.read_sql(query, connection)
 
        employee_skill_new= pd.merge(employee_skill,df_skills, on = ['Skill_Name'],how= 'inner')
        employee_skill_new= employee_skill_new.drop(employee_skill_new.columns[1],axis= 1)
        employee_stack= employee_skill_new.drop(employee_skill_new.columns[1], axis= 1) 
        print(employee_skill_new)

        # Filter for entries in Stack that are either "Data" or "WebDev"
        filtered_df = employee_stack[employee_stack['Stack'].isin(['Data', 'WebDev'])]
        
        # Count the occurrences of each stack type per employee
        counts = filtered_df.groupby(['Emp_ID', 'Stack']).size().unstack(fill_value=0)
        
        # Rename columns for clarity
        counts.columns.name = 'Stack'
        counts = counts.rename(columns={'Data': 'Data_Count', 'WebDev': 'WebDev_Count'})

        counts = counts.reset_index()

        skill_level_data= []

        for index, row in counts.iterrows():
            if row['WebDev_Count'] < 3 and row['Data_Count'] >= 3:

                if row['Data_Count'] >= 3 and row['Data_Count'] <= 4:
                    skill_level_data.append({'Emp_ID': row['Emp_ID'], 'Stack': 'Data', 'Skill_Level': "L1"})
                elif row['Data_Count'] > 4 and row['Data_Count'] <=8:
                    skill_level_data.append({'Emp_ID': row['Emp_ID'], 'Stack': 'Data', 'Skill_Level': 'L2'})
                elif row['Data_Count'] > 8:
                    skill_level_data.append({'Emp_ID': row['Emp_ID'], 'Stack': 'Data', 'Skill_Level': 'L3'})

            elif row['WebDev_Count'] >= 3 and row['Data_Count'] < 3:

                if row['WebDev_Count'] == 4:
                    skill_level_data.append({'Emp_ID': row['Emp_ID'], 'Stack': 'WebDev', 'Skill_Level': "L1"})
                elif row['WebDev_Count'] ==5:
                    skill_level_data.append({'Emp_ID': row['Emp_ID'], 'Stack': 'WebDev', 'Skill_Level': 'L2'})
                elif row['WebDev_Count'] == 5:
                    skill_level_data.append({'Emp_ID': row['Emp_ID'], 'Stack': 'WebDev', 'Skill_Level': 'L3'})

            elif row['WebDev_Count'] >= 3 and row['Data_Count'] >= 3:
                total_count= row['Data_Count'] + row['Data_Count']
                if total_count >= 6 and total_count <=11:
                    skill_level_data.append({'Emp_ID': row['Emp_ID'], 'Stack': 'Data and WebDev', 'Skill_Level': "L1"})
                elif total_count > 11 and total_count <=15:
                    skill_level_data.append({'Emp_ID': row['Emp_ID'], 'Stack': 'Data and WebDev', 'Skill_Level': 'L2'})
                elif total_count > 15:
                    skill_level_data.append({'Emp_ID': row['Emp_ID'], 'Stack': 'Data and WebDev', 'Skill_Level': 'L3'})
            
            elif row['WebDev_Count'] < 3 and row['Data_Count'] < 3:
                skill_level_data.append({'Emp_ID': row['Emp_ID'], 'Stack': 'Pool', 'Skill_Level': "No Rank"})

        skill_level_df = pd.DataFrame(skill_level_data)
        employees_new = pd.merge(employees, skill_level_df, on = ['Emp_ID'],how= 'left')
        
        # for entry in table Employees
        emp_ids = employees_new['Emp_ID'].tolist()
 
        # Check if any of the Emp_IDs already exists in the database
        check_query = "SELECT Emp_ID FROM Employees WHERE Emp_ID IN %s"
        with connection.cursor() as cursor:
            cursor.execute(check_query, (tuple(emp_ids),))
            existing_ids = set(row[0] for row in cursor.fetchall())
 
        # Determine if there are any new Emp_IDs
        new_rows = employees_new[~employees_new['Emp_ID'].isin(existing_ids)]
 
        if new_rows.empty:
            print("Data already exists for all Emp_IDs in the DataFrame.")
        else:
            # Insert new rows into the database
            sql_query = """INSERT INTO Employees(Emp_Id, Emp_Name, Email_ID, 
            Experience, Grade, Bench_Status, Bench_Duration, Employment_Status, 
            Communication_Level, Stack, Skill_Level) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            with connection.cursor() as cursor:
                for index, row in new_rows.iterrows():
                    values = tuple(row)
                    cursor.execute(sql_query, values)
                connection.commit()
 
    def upload_python_training():
        # Collect Emp_ID and Assessment_Date pairs from the DataFrame
        emp_assessment_pairs = list(zip(python_training.iloc[:, 1], python_training.iloc[:, 2], python_training.iloc[:, -2]))
 
        # Check if any of the Emp_ID and Assessment_Date pairs already exists in the database
        check_query = """
            SELECT Emp_ID, Test_Name, Assessment_Date FROM Python_Training
            WHERE (Emp_ID, Test_Name, Assessment_Date) IN %s
        """
        with connection.cursor() as cursor:
            cursor.execute(check_query, (tuple(emp_assessment_pairs),))
            existing_pairs = set(cursor.fetchall())  # Fetch all existing pairs
 
        # Determine if there are any new pairs
        new_rows = python_training[
            ~python_training.apply(lambda row: (row[1], row[2], row[-2]) in existing_pairs, axis=1)
        ]
 
        if new_rows.empty:
            print("Data already exists for all Emp_ID, Test_Name and Assessment_Date combinations in the DataFrame.")
        else:
            # Insert new rows into the database
            sql_query = "INSERT INTO Python_Training VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            with connection.cursor() as cursor:
                for index, row in new_rows.iterrows():
                    values = tuple(row)
                    cursor.execute(sql_query, values)
                connection.commit()
 
    def upload_employee_skills():
        query_a = "SELECT * FROM Skills"
        df_skills_a = pd.read_sql(query_a, connection)
 
        employee_skill_new_a= pd.merge(employee_skill,df_skills_a, on = ['Skill_Name'],how= 'inner')
        employee_skill_new_a= employee_skill_new_a.drop(employee_skill_new_a.columns[1],axis= 1)
 
        # Collect Emp_ID and Skill_ID pairs from the DataFrame
        emp_skill_pairs_a = list(zip(employee_skill_new_a.iloc[:, 0], employee_skill_new_a.iloc[:, 1]))
 
        # Check if any of the Emp_ID and skills pairs already exists in the database
        check_query_a = """
            SELECT Emp_ID, Skill_ID FROM Employee_Skills
            WHERE (Emp_ID, Skill_ID) IN %s
        """
        with connection.cursor() as cursor:
            cursor.execute(check_query_a, (tuple(emp_skill_pairs_a),))
            existing_pairs_a = set(cursor.fetchall())  # Fetch all existing pairs
 
        # Determine if there are any new pairs
        new_rows_a = employee_skill_new_a[
            ~employee_skill_new_a.apply(lambda row: (row[0], row[1]) in existing_pairs_a, axis=1)
        ]

        clean_new_rows_a= new_rows_a
        for column in new_rows_a.columns[0:2]:   
            clean_new_rows_a[f'{column}'] = clean_new_rows_a[f'{column}'].astype(int)

        clean_new_rows_a= clean_new_rows_a.drop(columns=['Stack'])
 
        if clean_new_rows_a.empty:
            print("Data already exists for all Emp_ID and Skill_ID combinations in the CSV.")
        else:
            # Insert new rows into the database
            sql_query_a = "INSERT INTO Employee_Skills VALUES (%s, %s)"
            with connection.cursor() as cursor:
                for index, row in clean_new_rows_a.iterrows():
                    values_a = tuple(row)
                    cursor.execute(sql_query_a, values_a)
                connection.commit()
 
    def upload_training_schedule():
        # for entry in table training_schedule
        team_ids = training_schedule['Team_ID'].tolist()
 
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
