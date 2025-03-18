import urllib.request
import json
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def fetch_data(start_date, end_date):
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
        print(f"Fetching data from {start_date} to {end_date}: {response.getcode()}")

        response_data = response.read().decode('utf-8')

        # Parse the response data as JSON
        json_data = json.loads(response_data)
        
        df = pd.DataFrame(json_data)

        # Flatten the JSON data using the 'return' column
        flattened_data = pd.json_normalize(df['return']['Actual Forecast Report'])
        
        # Extract relevant columns
        out = pd.DataFrame()
        out['begin_datetime_mpt'] = flattened_data['begin_datetime_mpt']
        out['alberta_internal_load'] = flattened_data['alberta_internal_load']
        out['forecast_alberta_internal_load'] = flattened_data['forecast_alberta_internal_load']

        return out

    except Exception as e:
        print(f"Error fetching data from {start_date} to {end_date}: {e}")
        return pd.DataFrame()

# Define the date range
end_date = datetime.today() - relativedelta(days=1)
start_date = end_date - relativedelta(years=3)

# Fetch data in chunks of 1 year
chunk_start_date = start_date
all_data = pd.DataFrame()

while chunk_start_date < end_date:
    chunk_end_date = min(chunk_start_date + relativedelta(years=1), end_date)
    chunk_start_str = chunk_start_date.strftime('%Y-%m-%d')
    chunk_end_str = chunk_end_date.strftime('%Y-%m-%d')

    # Fetch data for the current chunk
    chunk_data = fetch_data(chunk_start_str, chunk_end_str)

    # Concatenate the chunk to the main DataFrame
    all_data = pd.concat([all_data, chunk_data], ignore_index=True)

    # Move to the next chunk
    chunk_start_date = chunk_end_date + relativedelta(days=1)

# Save the concatenated data to a CSV file
output_file = f'/home/kevin/Downloads/BESS/Jobs/Retraining/data/raw/AIL_{start_date.strftime("%Y%m%d")}_{end_date.strftime("%Y%m%d")}.csv'
all_data.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")