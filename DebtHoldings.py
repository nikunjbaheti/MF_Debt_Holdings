import requests
import csv

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
                    csvwriter.writerow(json_data['portfolio'][0].keys())

                # Iterate through portfolio items and write rows
                for item in json_data['portfolio']:
                    csvwriter.writerow(item.values())

            print(f'Data for fincode={dynamic_number} successfully fetched and appended to {output_csv_filename}')

        except requests.exceptions.RequestException as e:
            print(f'Error fetching data from {url}: {e}')

if __name__ == "__main__":
    fetch_json_and_save_csv()
