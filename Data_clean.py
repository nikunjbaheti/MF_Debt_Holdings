import pandas as pd
import requests
from io import StringIO

# Function to replace "Ltd" and "Ltd." with "Limited" and convert to proper case
def clean_and_proper_case(row):
    return row.str.replace('Ltd.', 'Limited', case=False).str.replace('Ltd', 'Limited', case=False).str.title()

# Function to remove "EQ - " from all columns
def remove_eq_prefix(col):
    return col.str.replace('EQ - ', '', case=False)

# Function to remove double quotes from all columns
def remove_double_quotes(col):
    return col.str.replace('"', '')

# Function to perform modifications on a given CSV URL
def modify_csv_file(csv_url, output_file_path):
    # Fetch the CSV file from the URL
    response = requests.get(csv_url)
    csv_data = response.text

    # Read the CSV data using pandas
    df = pd.read_csv(StringIO(csv_data), delimiter='\t')

    # Remove "EQ - " from all columns
    df = df.apply(remove_eq_prefix)

    # Apply the replacement function and proper case conversion to all columns
    df = df.apply(clean_and_proper_case)

    # Remove double quotes from all columns
    df = df.apply(remove_double_quotes)

    # Write the modified data back to a new CSV file
    df.to_csv(output_file_path, sep='\t', index=False)
    print(f"Modification complete. Data written to {output_file_path}")

# Modify the first CSV file (StkCode.csv)
csv_url_stk = 'https://raw.githubusercontent.com/nikunjbaheti/MF_Debt_Holdings/main/Debt%20Holdings.csv'
output_file_path_stk = 'modified_Debt_Holdings.csv'
modify_csv_file(csv_url_stk, output_file_path_stk)
