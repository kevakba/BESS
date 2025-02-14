import urllib.request
import json
from datetime import datetime

# Define start_date and end_date as datetime objects
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

# Format the dates as strings in YYYY-MM-DD format
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

try:
    # Construct the URL with the provided dates
    url = f"https://apimgw.aeso.ca/public/poolprice-api/v1.1/price/poolPrice?startDate={start_date_str}&endDate={end_date_str}"

    hdr = {
        # Request headers
        'Cache-Control': 'no-cache',
        'API-KEY': 'ff8bd8112f6942ac97bb08cc88d0deae',
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())

    # Read and decode the response
    response_data = response.read().decode('utf-8')
    
    # Parse the response data as JSON
    json_data = json.loads(response_data)
    
    # Save the JSON data to a file
    output_file = f'/home/kevin/Downloads/BESS/data/raw/price_{start_date_str.replace("-", "")}_{end_date_str.replace("-", "")}.json'
    with open(output_file, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

except Exception as e:
    print(e)