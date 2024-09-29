import requests
import csv
from datetime import datetime

def fetch_numbers_from_csv(file_path):
    try:
        # Read the CSV file and extract the first column as dynamic numbers
        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            # Assuming the dynamic numbers are in the first column
            numbers = [row[0] for row in csvreader]
        
        return numbers

    except FileNotFoundError as e:
        print(f'Error: {file_path} not found: {e}')
        return []

def split_and_extend_rows(item):
    # Split fields that contain comma-separated values
    holdpercentage = item.get("holdpercentage", "").split(',')
    longname = item.get("longname", "").split(',')
    maturity_date = item.get("maturity_date", "").split(',')
    mktval = item.get("mktval", "").split(',')

    # Parse and format the invdate to DD-MM-YYYY
    try:
        invdate = datetime.strptime(item.get('invdate', ''), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d-%m-%Y")
    except ValueError:
        invdate = item.get('invdate', '')  # Keep original if parsing fails

    max_length = max(len(holdpercentage), len(longname), len(maturity_date), len(mktval))
    
    rows = []
    for i in range(max_length):
        row = {
            'amc': item.get('amc', ''),
            'schemecode': item.get('schemecode', ''),
            'invdate': invdate,  # Use the formatted date
            'holdpercentage': holdpercentage[i] if i < len(holdpercentage) else holdpercentage[-1],
            'aum': item.get('aum', ''),
            's_name': item.get('s_name', ''),
            'longname': longname[i] if i < len(longname) else longname[-1],
            'maturity_date': maturity_date[i] if i < len(maturity_date) else maturity_date[-1],
            'mktval': mktval[i] if i < len(mktval) else mktval[-1]
        }
        rows.append(row)
    
    return rows

def fetch_json_and_save_csv():
    # Path to StkCode.csv file
    stkcode_csv_path = 'StkCode.csv'

    # Fetch dynamic numbers from the CSV file
    dynamic_numbers = fetch_numbers_from_csv(stkcode_csv_path)

    if not dynamic_numbers:
        print('No dynamic numbers fetched. Exiting.')
        return

    # Specify the CSV file name for output
    output_csv_filename = 'Debt Holdings.csv'

    # Clear the contents of the output CSV file before appending new data
    with open(output_csv_filename, 'w') as csvfile:
        pass  # This will create or clear the file

    for dynamic_number in dynamic_numbers:
        # Construct the URL with the dynamic number
        url = f'https://www.rupeevest.com/mf_stock_portfolio/show_portfolio?fincode={dynamic_number}'

        try:
            # Fetch JSON data from the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses

            # Parse JSON data
            json_data = response.json()

            # Append JSON data to CSV file
            with open(output_csv_filename, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)

                # Check if the CSV file is empty, write header if needed
                if csvfile.tell() == 0:
                    csvwriter.writerow([
                        'amc', 'schemecode', 'invdate', 'holdpercentage', 
                        'aum', 's_name', 'longname', 'maturity_date', 'mktval'
                    ])

                # Iterate through portfolio items and write rows
                for item in json_data['portfolio']:
                    # Process and split the rows based on comma-separated values
                    extended_rows = split_and_extend_rows(item)
                    for row in extended_rows:
                        csvwriter.writerow(row.values())

        except requests.exceptions.RequestException as e:
            pass
            # print(f'Error fetching data from {url}: {e}')

if __name__ == "__main__":
    fetch_json_and_save_csv()
    
