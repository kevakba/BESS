import urllib.request
import json
import pandas as pd

# Define start_date and end_date
start_date = '2020-01-01'
end_date = '2020-12-31'

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
    # print(df['return']['Actual Forecast Report'])
    # Flatten the JSON data using the 'return' column
    flattened_data = pd.json_normalize(df['return']['Actual Forecast Report'])
    
    # flattened_data = flattened_data.T
    # print(flattened_data.head())
    # out['begin_datetime_mpt'] = flattened_data[0].apply(lambda x: x['begin_datetime_mpt'])
    # out['alberta_internal_load'] = flattened_data[0].apply(lambda x: x['alberta_internal_load'])
    # out['forecast_alberta_internal_load'] = flattened_data[0].apply(lambda x: x['forecast_alberta_internal_load'])
    
    # print(out.head())
    out['begin_datetime_mpt'] = flattened_data['begin_datetime_mpt']
    out['alberta_internal_load'] = flattened_data['alberta_internal_load']
    out['forecast_alberta_internal_load'] = flattened_data['forecast_alberta_internal_load']
    # print(out.head())
    out.to_csv(f'/home/kevin/Downloads/BESS/data/raw/2020/AIL_{start_date.replace("-", "")}_{end_date.replace("-", "")}.csv')

except Exception as e:
    print(e)