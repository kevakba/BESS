import urllib.request
import json
import pandas as pd

# Define start_date and end_date
start_date = '2025-03-10'
end_date = '2025-03-10'

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
    out['forecast_alberta_internal_load'] = flattened_data['forecast_alberta_internal_load']

    out.to_csv(f'/home/kevin/Downloads/BESS/data/raw/forecast/AIL_{start_date.replace("-", "")}_{end_date.replace("-", "")}.csv')

except Exception as e:
    print(e)