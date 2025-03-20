import urllib.request
import json
from datetime import datetime, timedelta
import pandas as pd

# Define start_date and end_date as datetime objects
current_date = datetime.now()
next_date = current_date + timedelta(days=-2)
start_date = next_date.strftime('%Y-%m-%d')
end_date = current_date.strftime('%Y-%m-%d')

# print(current_date, next_date)
# print(start_date, end_date)

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
    out['begin_datetime_mpt'] = flattened_data['begin_datetime_mpt']
    out['forecast_pool_price'] = flattened_data['pool_price']
    out['rolling_30day_avg_price'] = flattened_data['rolling_30day_avg']

    out = out[(pd.to_datetime(out.begin_datetime_mpt) <= current_date) & (pd.to_datetime(out.begin_datetime_mpt) >= next_date) ]
    out['begin_datetime_mpt'] = pd.to_datetime(out['begin_datetime_mpt'])
    out['begin_datetime_mpt'] = out['begin_datetime_mpt'] + timedelta(days=1)
    out.to_csv(f'/home/kevin/Downloads/BESS/Jobs/Inferencing/data/raw/price_{start_date.replace("-", "")}_{end_date.replace("-", "")}.csv')

except Exception as e:
    print(e)



