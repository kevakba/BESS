import pandas as pd
import time
from datetime import datetime, timedelta

url = 'http://ets.aeso.ca/Market/Reports/Manual/Operations/prodweb_reports/wind_solar_forecast/wind_rpt_longterm.csv'
# Get the current date and add one day to it
current_date = datetime.now()
next_date = current_date + timedelta(days=1)


# date_ = '2025-03-10'
result_df = pd.DataFrame()

while result_df.empty:
    try:
        df = pd.read_csv(url)
        df = df[(pd.to_datetime(df['Forecast Transaction Date']) > current_date) & (pd.to_datetime(df['Forecast Transaction Date']) < next_date) ]
        result_df['datetime_'] = df['Forecast Transaction Date']
        result_df['wind_generation'] = df['Most Likely']
        result_df.reset_index(drop=True, inplace=True)
        # print(result_df)
    except Exception as e:
        print(f"Error fetching data: {e}. Retrying in 5 seconds...")
        time.sleep(5)
    

current_date = current_date.strftime('%Y-%m-%d')
next_date = next_date.strftime('%Y-%m-%d')
result_df.to_csv(f'/home/kevin/Downloads/BESS/Jobs/Inferencing/data/raw/wind_generation_{str(current_date).replace("-", "")}_{str(next_date).replace("-", "")}.csv')