# %% [markdown]
# #### Library

# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz

# Set pandas options to display all rows and columns
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

import os

# %% [markdown]
# #### Data Loading

# %%
# Folder containing CSV files
folder_path = "Jobs/Inferencing/data/raw" 

df_list = []
# Loop through each file in the folder
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        df_name = os.path.splitext(file)[0].split('20')[0]  # Remove the .csv extension for naming
        globals()[df_name] = pd.read_csv(file_path)  # Create a variable dynamically
        print(f"Loaded DataFrame: {df_name}, Shape: {globals()[df_name].shape}")
        df_list.append(df_name)

# Sort the list of DataFrames
df_list.sort()


# %%
for df_name in df_list:
    print(f"\nDataFrame: {df_name}")
    # display(globals()[df_name].head())

# %% [markdown]
# #### Column Name Adjustment

# %%
for df_name in df_list:
    print(f"\nDataFrame: {df_name}")
    globals()[df_name].drop(['Unnamed: 0'], axis=1, inplace=True)
    # display(globals()[df_name].head())

# %%
# Rename columns
price_.rename(columns={'begin_datetime_mpt': 'datetime_'}, inplace=True)

AIL_.rename(columns={'begin_datetime_mpt': 'datetime_'}, inplace=True)

solar_generation_.rename(columns={'Date (MPT)': 'datetime_', 'Volume':'solar_generation'}, inplace=True)

wind_generation_.rename(columns={'Date (MPT)': 'datetime_', 'Volume':'wind_generation'}, inplace=True)

temperature_calgary_.rename(columns={'Timestamp_mst': 'datetime_', 'Temperature (°C)':'temp_calgary'}, inplace=True)

temperature_edmonton_.rename(columns={'Timestamp_mst': 'datetime_', 'Temperature (°C)':'temp_edmonton'}, inplace=True)

temperature_fortmc_.rename(columns={'Timestamp_mst': 'datetime_', 'Temperature (°C)':'temp_fortmc'}, inplace=True)

windspeed_calgary_.rename(columns={'Timestamp_mst': 'datetime_', 'Wind Speed (km/h)':'ws_calgary'}, inplace=True)

windspeed_edmonton_.rename(columns={'Timestamp_mst': 'datetime_', 'Wind Speed (km/h)':'ws_edmonton'}, inplace=True)

windspeed_fortmc_.rename(columns={'Timestamp_mst': 'datetime_', 'Wind Speed (km/h)':'ws_fortmc'}, inplace=True)

# %%
for df_name in df_list:
    print(f"\nDataFrame: {df_name}")
    # display(globals()[df_name].head())

# %%
# convert columns to datetime
for df_name in df_list:
    print(f"\nDataFrame: {df_name}")
    try:
        globals()[df_name]['datetime_'] = pd.to_datetime(globals()[df_name]['datetime_'])
        # display(globals()[df_name].head())
    except:
        globals()[df_name]['datetime_'] = pd.to_datetime(globals()[df_name]['Timestamp'])
        globals()[df_name].drop(['Timestamp'], axis=1, inplace=True)
        # display(globals()[df_name].head())

# %%
# Initialize the merged dataframe with the first dataframe in the list
merged_df = globals()[df_list[0]]

# Loop through the remaining dataframes and merge them one by one
for df_name in df_list[1:]:
    merged_df = merged_df.merge(globals()[df_name], on='datetime_', how='outer')

# Display the merged dataframe
# display(merged_df.head())

# %%
merged_df.info()

# %%
merged_df.shape

# %%
merged_df.isnull().sum()

# %% [markdown]
# #### Feature Engineering

# %% [markdown]
# ##### time based variables

# %%
merged_df['hour_of_day'] = merged_df['datetime_'].dt.hour
merged_df['day_of_week'] = merged_df['datetime_'].dt.dayofweek
merged_df['day_of_month'] = merged_df['datetime_'].dt.day
# Calculate the week of the month (from 1 to 5)
merged_df['week_of_month'] = merged_df['datetime_'].apply(lambda x: (x.day - 1) // 7 + 1)
merged_df['month'] = merged_df['datetime_'].dt.month
merged_df['year'] = merged_df['datetime_'].dt.year

# Display the updated dataframe
# display(merged_df.head())

# %% [markdown]
# ##### seasonality

# %%
# Define a function to determine the season
def get_season(month):
    if month in [5, 6, 7, 8, 9]:
        return 0 # Summer
    else:
        return 1 # Winter

# Apply the function to create a new column 'season'
merged_df['is_winter'] = merged_df['month'].apply(get_season)

# Display the updated dataframe
# display(merged_df.head())

# %% [markdown]
# ##### pool_price_lagged_values_till_24_hours

# %%
def generate_lagged_features(df, column, num_lags):
    for lag in range(1, num_lags + 1):
        df[f'pool_price_lag_{lag}'] = df[column].shift(lag)
    return df

# Generate 24-hour lagged values for the pool_price column
merged_df = generate_lagged_features(merged_df, 'forecast_pool_price', 24)

# Display the updated dataframe
# display(merged_df.head())

# %% [markdown]
# ##### AIL_lagged_values_till_24_hours

# %%
def generate_lagged_features(df, column, num_lags):
    for lag in range(1, num_lags + 1):
        df[f'{column}_lag_{lag}'] = df[column].shift(lag)
    return df

# Generate 24-hour lagged values for the AIL column
merged_df = generate_lagged_features(merged_df, 'alberta_internal_load', 24)

# Display the updated dataframe
# display(merged_df.head())

# %%
# Get the current time in MST
mst_timezone = pytz.timezone('MST')
filter_time = datetime.now(mst_timezone)

# Convert to string format if needed
filter_time_str = filter_time.strftime('%Y-%m-%d %H:%M:%S')
print(f"Filtering data from: {filter_time_str}")
# Apply the filter
merged_df = merged_df[merged_df['datetime_'] >= filter_time_str]

merged_df.isnull().sum().sort_values(ascending=False) 

# %%
# forward fill the NA values
merged_df.fillna(method='ffill', inplace=True)

# %% [markdown]
# #### Save Data

# %%
merged_df.to_csv('Jobs/Inferencing/data/raw/merged_df.csv', index=False)


