# %% [markdown]
# #### Library

# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import glob

# %% [markdown]
# #### Generation

# %%
# Get list of all CSV files in the directory
path = 'data/large_files/Generation Data/'
csv_files = glob.glob(path+'*.csv')

# Load all CSV files into a list of dataframes
dataframes = [pd.read_csv(file) for file in csv_files]

# concatenate all dataframes into a single dataframe
df = pd.concat(dataframes, axis=0)

# convert to datetime
df['Date (MPT)'] = pd.to_datetime(df['Date (MPT)'])

print(df.shape)

# %%
wind_generation = df[(df['Fuel Type'] == 'WIND')]
wind_generation = wind_generation.groupby('Date (MPT)')['Volume'].sum().reset_index()
wind_generation.sort_values(by='Date (MPT)', inplace=True)
# wind_generation[wind_generation['Date (MPT)'].dt.year == 2019].to_csv('/home/kevin/Downloads/BESS/Jobs/Retraining/data/raw/wind_generation_2019.csv')
wind_generation.to_csv('Jobs/Retraining/data/raw/wind_generation.csv')

# %%
solar_generation = df[(df['Fuel Type'] == 'SOLAR')]
solar_generation = solar_generation.groupby('Date (MPT)')['Volume'].sum().reset_index()
solar_generation.sort_values(by='Date (MPT)', inplace=True)
# solar_generation[solar_generation['Date (MPT)'].dt.year == 2019].to_csv('/home/kevin/Downloads/BESS/Jobs/Retraining/data/raw/solar_generation_2019.csv')
solar_generation.to_csv('Jobs/Retraining/data/raw/solar_generation.csv')


