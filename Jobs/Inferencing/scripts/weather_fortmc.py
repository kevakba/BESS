import requests
from datetime import datetime, timedelta
import pandas as pd

def get_weather_forecast(latitude, longitude):
    """
    Fetches the next 24-hour temperature and wind speed forecast for a given location.
    #Calgary --> latitude=51.0447, longitude=-114.0719
    #Edmonton --> latitude=53.5501, longitude=-113.4687
    #FortMcMurray --> latitude=56.7268, longitude=-111.381
    
    :param latitude: Latitude of the location (default: Calgary, Canada)
    :param longitude: Longitude of the location (default: Calgary, Canada)
    :return: Pandas DataFrame with columns: ['Timestamp', 'Temperature (°C)', 'Wind Speed (km/h)']
    """
    # Define the API endpoint and parameters
    endpoint = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': ['temperature_2m', 'windspeed_10m'],
        'timezone': 'America/Edmonton'
    }

    # Make the API request
    response = requests.get(endpoint, params=params)
    
    # Check for successful response
    if response.status_code != 200:
        print("Error fetching data:", response.text)
        return None
    
    data = response.json()
    
    # Extract forecast data
    hourly_times = data['hourly']['time']  # Next 48 hours
    hourly_temps = data['hourly']['temperature_2m']
    hourly_windspeeds = data['hourly']['windspeed_10m']

    # Convert time to datetime format
    timestamps = [datetime.fromisoformat(time) for time in hourly_times]

    # Create a Pandas DataFrame
    forecast_df = pd.DataFrame({
        'Timestamp': timestamps,
        'Temperature (°C)': hourly_temps,
        'Wind Speed (km/h)': hourly_windspeeds
    })
    current_date = datetime.now()
    forecast_df = forecast_df[(pd.to_datetime(forecast_df.Timestamp) > current_date) & (pd.to_datetime(forecast_df.Timestamp) < current_date+ timedelta(hours=24)) ]
    return forecast_df


df = get_weather_forecast(latitude=56.7268, longitude=-111.381)
start_date = df['Timestamp'].min()
end_date = df['Timestamp'].max()

#Convert the 'Timestamp' column to datetime format and set timezone to UTC
df['Timestamp'] = df['Timestamp'].dt.tz_localize('America/Edmonton').dt.tz_convert('UTC')
df['Timestamp'] = df['Timestamp'].dt.strftime('%Y-%m-%d %H:00')

df[['Timestamp', 'Temperature (°C)']].to_csv(f'Jobs/Inferencing/data/raw/temperature_fortmc_{str(start_date).split(" ")[0].replace("-", "")}_{str(end_date).split(" ")[0].replace("-", "")}.csv')


df[['Timestamp', 'Wind Speed (km/h)']].to_csv(f'Jobs/Inferencing/data/raw/windspeed_fortmc_{str(start_date).split(" ")[0].replace("-", "")}_{str(end_date).split(" ")[0].replace("-", "")}.csv')