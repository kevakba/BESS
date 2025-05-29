import pandas as pd
import time
from datetime import datetime, timedelta
from backports.zoneinfo import ZoneInfo

url = 'http://ets.aeso.ca/Market/Reports/Manual/Operations/prodweb_reports/wind_solar_forecast/wind_rpt_longterm.csv'
# Get the current date and add one day to it
current_date = datetime.now(ZoneInfo('UTC')) 
current_date = current_date.replace(tzinfo=None)
next_date = current_date + timedelta(days=1)
# print(type(current_date))
current_date = current_date.strftime('%Y-%m-%d %H:00')
next_date = next_date.strftime('%Y-%m-%d %H:00')


# date_ = '2025-03-10'
result_df = pd.DataFrame()

while result_df.empty:
    try:
        df = pd.read_csv(url)
        df['Forecast Transaction Date'] = pd.to_datetime(df['Forecast Transaction Date'], format='%Y-%m-%d %H:00')
        #Convert the 'Timestamp' column to datetime format and set timezone to UTC
        df['Forecast Transaction Date'] = df['Forecast Transaction Date'].dt.tz_localize('America/Edmonton').dt.tz_convert('UTC')
        df['Forecast Transaction Date'] = df['Forecast Transaction Date'].dt.strftime('%Y-%m-%d %H:00')
        df = df[(df['Forecast Transaction Date'] > current_date) & (df['Forecast Transaction Date'] < next_date) ]
        result_df['datetime_'] = df['Forecast Transaction Date']
        result_df['wind_generation'] = df['Most Likely']
        result_df.reset_index(drop=True, inplace=True)
        # print(result_df)
    except Exception as e:
        print(f"Error fetching data: {e}. Retrying in 5 seconds...")
        time.sleep(5)

    break

#Convert the 'Timestamp' column to datetime format and set timezone to UTC    
# result_df['datetime_'] = pd.to_datetime(result_df['datetime_'], format='%Y-%m-%d %H:00')
# result_df['datetime_'] = result_df['datetime_'].dt.tz_localize('America/Edmonton').dt.tz_convert('UTC')
# result_df['datetime_'] = result_df['datetime_'].dt.strftime('%Y-%m-%d %H:00')

# current_date = current_date.strftime('%Y-%m-%d')
# next_date = next_date.strftime('%Y-%m-%d')
result_df.to_csv(f"Jobs/Inferencing/data/raw/wind_generation_{current_date.split(' ')[0].replace('-', '')}_{next_date.split(' ')[0].replace('-', '')}.csv")