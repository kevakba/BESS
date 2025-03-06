import urllib.request
import json
from datetime import datetime
import pandas as pd

# Define start_date and end_date as datetime objects
start_date = '2025-03-06'
end_date = '2025-03-06'

try:
    # Construct the URL with the provided dates
    url = f"https://apimgw.aeso.ca/public/poolprice-api/v1.1/price/poolPrice?startDate={start_date}&endDate={end_date}"

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
    
    df = pd.DataFrame(json_data)

    # Initialize an empty DataFrame to store the output
    out = pd.DataFrame()

    # Flatten the JSON data using the 'return' column
    flattened_data = pd.json_normalize(df['return']['Pool Price Report'])
    # print(flattened_data)
    out['begin_datetime_mpt'] = flattened_data['begin_datetime_mpt']
    out['forecast_pool_price'] = flattened_data['forecast_pool_price']
    out['rolling_30day_avg'] = flattened_data['rolling_30day_avg']

    out.to_csv(f'/home/kevin/Downloads/BESS/data/raw/forecast/price_{start_date.replace("-", "")}_{end_date.replace("-", "")}.csv')

except Exception as e:
    print(e)



