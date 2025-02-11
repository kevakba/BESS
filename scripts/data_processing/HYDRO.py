# import pandas as pd

# # Load the JSON data
# input_file = '/home/kevin/Downloads/BESS/data/energy_generation_20240601_20240630.json'
# data = pd.read_json(input_file)
# print(data.head())
# # Filter the DataFrame for fuel_type as HYDRO
# hydro_data = data[data['fuel_type'] == 'HYDRO']

# # Select the begin_datetime_mpt and AC columns
# hydro_ac_df = hydro_data[['begin_datetime_mpt', 'AC']]

# # Print the resulting DataFrame
# print(hydro_ac_df.head())