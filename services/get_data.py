import pandas as pd

def csv_to_dataframe():
 
    hiring_data = pd.read_csv('''data/hiring_data.csv''')
    training_data = pd.read_csv('''data/python_training_data.csv''')
    training_schedule_data= pd.read_csv('''data/training_schedule_data.csv''')
   
    # For Employee and Skills
    employees= hiring_data.iloc[:,:9]
    employee_skill= hiring_data.iloc[:,[0, -1]]
 
    # For Training data and training schedule
    python_training= training_data
    training_schedule= training_schedule_data
 
    return employees, employee_skill, python_training, training_schedule