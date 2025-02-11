########### Python 3.2 #############
import urllib.request, json
# print('Hello')
try:
    url = "https://apimgw.aeso.ca/public/poolprice-api/v1.1/price/poolPrice?startDate=2024-06-01&endDate=2024-12-31"

    hdr ={
    # Request headers
    'Cache-Control': 'no-cache',
    'API-KEY': 'ff8bd8112f6942ac97bb08cc88d0deae',
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())

    # print(response.read())
    # Read and decode the response
    response_data = response.read().decode('utf-8')
    
    # Parse the response data as JSON
    json_data = json.loads(response_data)
    
    # Save the JSON data to a file
    with open('/home/kevin/Downloads/BESS/data/price_01062024_31122024.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

except Exception as e:
    print(e)
####################################