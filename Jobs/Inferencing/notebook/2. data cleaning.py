# %%
# This notebook cleans the data and creates a new csv file with the cleaned data

# %% [markdown]
# #### Library

# %%
import pandas as pd
# Set pandas options to display all rows and columns
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import warnings

warnings.filterwarnings('ignore', category=pd.errors.PerformanceWarning)

# %% [markdown]
# #### Data Loading

# %%
df = pd.read_csv('Jobs/Inferencing/data/raw/merged_df.csv')

# %% [markdown]
# #### Data Cleaning

# %%
df.shape

# %%
df.head()

# %%
df.isnull().sum().sort_values(ascending=False)

# %%
# Filter columns that do not start with 'alberta' or 'pool'
filtered_columns = [col for col in df.columns if not col.startswith('alberta_internal_load_') and not col.startswith('pool_price_')]

# Select columns with more than 1 missing value
columns_with_missing_values = df[filtered_columns].isnull().sum()
columns_with_missing_values = columns_with_missing_values[columns_with_missing_values > 0]

# Display the columns with more than 1 missing value
print(columns_with_missing_values.index)

# %%
# # impute median for missing values

# for col in columns_with_missing_values.index:
#     df[col].fillna(df[col].median(), inplace=True)

# %%
# # fill NAN with bfill method
# lagged_columns = [f'pool_price_lag_{i}' for i in range(1, 25)] + [f'alberta_internal_load_lag_{i}' for i in range(1, 25)]

# df[lagged_columns] = df[lagged_columns].fillna(method='bfill')
# # Verify if NaN values are filled
# print(df[lagged_columns].isnull().sum().sort_values(ascending=False))

# %%
df.isnull().sum().sort_values(ascending=False)

# %%
df.drop('forecast_pool_price', axis=1, inplace=True)
df.rename(columns={'alberta_internal_load': 'forecast_alberta_internal_load'}, inplace=True)
print(df.datetime_.min(), '-------------------------to-------------------------', df.datetime_.max())

# %% [markdown]
# #### Save csv


# %%
df.to_csv('Jobs/Inferencing/data/cleaned/merged_df_cleaned.csv', index=False)


