import urllib.request
import json
from datetime import datetime, timedelta

# Define the start and end dates
start_date = datetime(2024, 6, 1)
end_date = datetime(2024, 6, 1)

# Function to get the last day of the month
def last_day_of_month(date):
    next_month = date.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)

# Loop through each month
current_date = start_date
while current_date <= end_date:
    month_start = current_date.replace(day=1)
    month_end = last_day_of_month(month_start)
    
    startDate = month_start.strftime('%Y-%m-%d')
    endDate = month_end.strftime('%Y-%m-%d')
    
    try:
        url = f"https://apimgw.aeso.ca/public/aiesgencapacity-api/v1/AIESGenCapacity?startDate={startDate}&endDate={endDate}"

        hdr = {
            'Cache-Control': 'no-cache',
            'API-KEY': 'ff8bd8112f6942ac97bb08cc88d0deae',
        }

        req = urllib.request.Request(url, headers=hdr)

        response = urllib.request.urlopen(req)
        print(f"Response code for {startDate} to {endDate}: {response.getcode()}")

        response_data = response.read().decode('utf-8')

        # Parse the response data as JSON
        json_data = json.loads(response_data)
        print('Data fetched successfully')

        # Save the JSON data to a file
        file_name = f'/home/kevin/Downloads/BESS/data/energy_generation_{startDate.replace("-", "")}_{endDate.replace("-", "")}.json'
        with open(file_name, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f"Data saved to {file_name}")

    except urllib.error.HTTPError as e:
        print(f"HTTP error for {startDate} to {endDate}: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL error for {startDate} to {endDate}: {e.reason}")
    except Exception as e:
        print(f"Unexpected error for {startDate} to {endDate}: {e}")

    # Move to the next month
    current_date = month_end + timedelta(days=1)