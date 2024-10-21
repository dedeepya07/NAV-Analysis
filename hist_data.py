import requests
from tqdm import tqdm
import time
from datetime import datetime, timedelta

# Function to generate all dates between start_date and end_date
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

# Function to fetch data for a specific date
def fetch_data(date):
    url = f"https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt={date}"
    response = requests.get(url)
    return response.text

# Date range
start_date = datetime.strptime('01-01-2020', '%d-%m-%Y')
end_date = datetime.strptime('31-08-2024', '%d-%m-%Y')

# Open the file to write data
with open('nav_data.txt', 'w') as file:
    for date in tqdm(daterange(start_date, end_date), desc="Fetching Data", unit="day"):
        # Format date as needed by the URL
        formatted_date = date.strftime('%d-%b-%Y')
        
        try:
            # Fetch data for the date
            data = fetch_data(formatted_date)
            file.write(f"Data for {formatted_date}:\n")
            file.write(data + "\n\n")
            time.sleep(0.5)  # To avoid overloading the server (optional)
        except Exception as e:
            print(f"Error fetching data for {formatted_date}: {e}")