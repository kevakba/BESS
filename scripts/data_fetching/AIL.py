import urllib.request
import json

# Define start_date and end_date
start_date = '2024-01-01'
end_date = '2024-12-31'

try:
    # Construct the URL with the provided dates
    url = f"https://apimgw.aeso.ca/public/actualforecast-api/v1/load/albertaInternalLoad?startDate={start_date}&endDate={end_date}"

    hdr = {
        # Request headers
        'Cache-Control': 'no-cache',
        'API-KEY': 'ff8bd8112f6942ac97bb08cc88d0deae',
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())

    response_data = response.read().decode('utf-8')

    # Parse the response data as JSON
    json_data = json.loads(response_data)
    
    # Save the JSON data to a file
    output_file = f'/home/kevin/Downloads/BESS/data/raw/AIL_{start_date.replace("-", "")}_{end_date.replace("-", "")}.json'
    with open(output_file, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
except Exception as e:
    print(e)