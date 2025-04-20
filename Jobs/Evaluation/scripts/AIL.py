import urllib.request
import json
import pandas as pd
from datetime import datetime, timedelta
import sys

# --- Argument Parsing ---
if len(sys.argv) != 3:
    print("Usage: python AIL.py <start_date: YYYY-MM-DD> <end_date: YYYY-MM-DD>")
    sys.exit(1)

start_date_str = sys.argv[1]
end_date_str = sys.argv[2]

# --- Validate Date Format ---
try:
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
except ValueError:
    print("❌ Invalid date format. Please use YYYY-MM-DD.")
    sys.exit(1)

# --- Format Dates for API ---
start_date = start_date.strftime('%Y-%m-%d')
end_date = end_date.strftime('%Y-%m-%d')

try:
    # Construct the URL with the provided dates
    url = f"https://apimgw.aeso.ca/public/actualforecast-api/v1/load/albertaInternalLoad?startDate={start_date}&endDate={end_date}"

    hdr = {
        # Request headers
        'Cache-Control': 'no-cache',
        'API-KEY': 'ff8bd8112f6942ac97bb08cc88d0deae',
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())

    response_data = response.read().decode('utf-8')

    # Parse the response data as JSON
    json_data = json.loads(response_data)
    
    df = pd.DataFrame(json_data)

    # Initialize an empty DataFrame to store the output
    out = pd.DataFrame()
    
    # Flatten the JSON data using the 'return' column
    flattened_data = pd.json_normalize(df['return']['Actual Forecast Report'])
    out['begin_datetime_mpt'] = flattened_data['begin_datetime_mpt'] 
    out['alberta_internal_load'] = flattened_data['alberta_internal_load']
    # print(out)
    # out = out[(pd.to_datetime(out.begin_datetime_mpt) >= current_date) & (pd.to_datetime(out.begin_datetime_mpt) <= next_date) ]

    out.to_csv(f'Jobs/Evaluation/data/actual/AIL.csv')

except Exception as e:
    print(e)