import requests
import json

# Define API endpoint
url = "https://api.weather.gc.ca/collections/climate-hourly/items"

# Set query parameters (example: station ID, date, format)
params = {
    "stationID": "50430",  # Replace with your desired station ID
    "year": 2024,
    "month": 2,
    "day": 1,
    "format": "json",  # Change to "csv" if needed
}

# Make GET request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    weather_data = response.json()
    # print(weather_data)  # Print JSON data
    # Save JSON data to a file
    with open("/home/kevin/Downloads/BESS/data/weather_data.json", "w") as file:
        json.dump(weather_data, file, indent=4)
    print("Weather data saved as JSON!")
else:
    print(f"Error: {response.status_code}, {response.text}")





