import pandas as pd
import time
from datetime import datetime, timedelta

url = 'http://ets.aeso.ca/Market/Reports/Manual/Operations/prodweb_reports/wind_solar_forecast/solar_rpt_longterm.csv'
# Get the current date and add one day to it
current_date = datetime.now()
next_date = current_date + timedelta(days=1)

result_df = pd.DataFrame()

while result_df.empty:
    try:
        df = pd.read_csv(url)
        df = df[(pd.to_datetime(df['Forecast Transaction Date']) > current_date) & (pd.to_datetime(df['Forecast Transaction Date']) < next_date) ]
        result_df['datetime_'] = df['Forecast Transaction Date']
        result_df['solar_generation'] = df['Most Likely']
        result_df.reset_index(drop=True, inplace=True)
        # print(result_df)
    except Exception as e:
        print(f"Error fetching data: {e}. Retrying in 5 seconds...")
        time.sleep(5)

    break

#Convert the 'Timestamp' column to datetime format and set timezone to UTC   
result_df['datetime_'] = pd.to_datetime(result_df['datetime_'], format='%Y-%m-%d %H:00')
result_df['datetime_'] = result_df['datetime_'].dt.tz_localize('America/Edmonton').dt.tz_convert('UTC')
result_df['datetime_'] = result_df['datetime_'].dt.strftime('%Y-%m-%d %H:00')

current_date = current_date.strftime('%Y-%m-%d')
next_date = next_date.strftime('%Y-%m-%d')
result_df.to_csv(f'Jobs/Inferencing/data/raw/solar_generation_{str(current_date).replace("-", "")}_{str(next_date).replace("-", "")}.csv')