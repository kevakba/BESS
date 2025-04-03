import urllib.request
import json
from datetime import datetime, timedelta
import pandas as pd

# Define start_date and end_date as datetime objects
current_date = datetime.now()
next_date = current_date + timedelta(days=-20)
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
    # print(flattened_data)
    out['begin_datetime_mpt'] = flattened_data['begin_datetime_mpt']
    out['begin_datetime_mpt'] = pd.to_datetime(out['begin_datetime_mpt'])
    out.rename(columns={'begin_datetime_mpt': 'datetime_'}, inplace=True)
    out['actual_pool_price'] = flattened_data['pool_price']
    # out['rolling_30day_avg_price'] = flattened_data['rolling_30day_avg']

    out = out[(pd.to_datetime(out.datetime_) <= current_date) & (pd.to_datetime(out.datetime_) >= next_date) ]
    
    # out['begin_datetime_mpt'] = out['begin_datetime_mpt'] + timedelta(days=1)
    # print('here........................................')
    out_old = pd.read_csv('Jobs/Validation/data/actual/price.csv')
    out = pd.concat([out_old, out], ignore_index=True)
    out.drop_duplicates(subset=['datetime_'], keep='last', inplace=True)
    out = out.sort_values(by='datetime_', ascending=True)
    out.reset_index(drop=True, inplace=True)
    out.to_csv(f'Jobs/Validation/data/actual/price.csv', index=False)

except Exception as e:
    print(e)



