########### Python 3.2 #############
import urllib.request, json

try:
    url = "https://apimgw.aeso.ca/public/currentsupplydemand-api/v1/csd/summary/current"

    hdr ={
    # Request headers
    'Cache-Control': 'no-cache',
    'API-KEY': 'ff8bd8112f6942ac97bb08cc88d0deae',
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())
    
    # Read and decode the response
    response_data = response.read().decode('utf-8')
    
    # Parse the response data as JSON
    json_data = json.loads(response_data)
    
    # Save the JSON data to a file
    with open('response.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    
    # Print the JSON data
    # print(json_data)
except Exception as e:
    print(e)
####################################