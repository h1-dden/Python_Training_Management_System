import pandas as pd

def create_template_file(filename):
  """
  Creates a template CSV file with only the header row from the original file.
  Args:
    filename: The name of the original CSV file.
  """

  # Read the original CSV file
  df = pd.read_csv(filename)

  # Extract the header row
  header_row = df.head(0)

  # Create the template filename
  template_filename = filename.split('.')[0] + '_template.csv'

  # Save the header row to the template file
  header_row.to_csv(template_filename, index=False)

# Example usage:
filename = r"training_schedule_data.csv"
#change filename for training_data and hiring_data
create_template_file(filename)