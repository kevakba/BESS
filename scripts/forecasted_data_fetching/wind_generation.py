import pandas as pd
import time

url = 'http://ets.aeso.ca/Market/Reports/Manual/Operations/prodweb_reports/wind_solar_forecast/wind_rpt_longterm.csv'
date_ = '2025-03-10'
result_df = pd.DataFrame()

while result_df.empty:
    try:
        df = pd.read_csv(url)
        result_df['datetime_'] = df[df['Forecast Transaction Date'].apply(lambda x: x.split(' ')[0]) == f'{date_}']['Forecast Transaction Date']
        result_df['wind_generation'] = df[df['Forecast Transaction Date'].apply(lambda x: x.split(' ')[0]) == f'{date_}']['Most Likely']
        result_df.reset_index(drop=True, inplace=True)
    except Exception as e:
        print(f"Error fetching data: {e}. Retrying in 5 seconds...")
        time.sleep(5)


result_df.to_csv(f'/home/kevin/Downloads/BESS/data/raw/forecast/wind_generation_{str(date_).replace("-", "")}_{str(date_).replace("-", "")}.csv')