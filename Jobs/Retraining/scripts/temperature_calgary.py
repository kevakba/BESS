import requests
import pandas as pd
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta

def get_hourly_temperature(climate_id, start_date, end_date):
  url = "https://api.weather.gc.ca/collections/climate-hourly/items"
  all_temp_data = []
  limit = 10000
  offset = 0
  

  while True:
    params = {
      "CLIMATE_IDENTIFIER": climate_id,
      "datetime": f"{start_date}/{end_date}",
      "limit": limit,
      "offset": offset,
      "f": "json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data['features']:
          break
        # for f in data['features']:
        #    print(f)
        for feature in data['features']:
            properties = feature['properties']
            all_temp_data.append({
                # 'Timestamp_utc': pd.to_datetime(properties['UTC_DATE'], utc=True),
                'Timestamp_mst': pd.to_datetime(properties['LOCAL_DATE']),
                'Temperature (degree C)': properties.get('TEMP', None)
            })
          
        offset += limit

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        break
    except Exception as err:
        print(f"Other error occurred: {err}")
        break
  temp_df = pd.DataFrame(all_temp_data)
  # print(temp_df.head())
  temp_df = temp_df.sort_values(by='Timestamp_mst')

  return temp_df
  
# Example
# CALGARY ID : 3031092
# EDMONTON ID: 3012205 or 3012206
# FORT MC ID: 3062696
climate_id = "3031092" 

# Define the date range
end_date = datetime.today() - relativedelta(days=1)
start_date = end_date - relativedelta(years=3)
end_date = end_date.strftime('%Y-%m-%d')
start_date = start_date.strftime('%Y-%m-%d')

# start_date = "2019-01-01T00:00:00Z"

# end_date = "2020-12-31T23:00:00Z"

# print(start_date.split("T")[0].replace("-", ""))
# print(end_date.split("T")[0].replace("-", ""))
df = get_hourly_temperature(climate_id, start_date, end_date)
# print(df)
df.to_csv(f'/home/kevin/Downloads/BESS/Jobs/Retraining/data/raw/temperature_calgary_{start_date.split("T")[0].replace("-", "")}_{end_date.split("T")[0].replace("-", "")}.csv')


