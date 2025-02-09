########### Python 3.2 #############
import urllib.request, json
print("Inter-Tie Capacity")
try:
    url = "https://apimgw.aeso.ca/public/itc/v1/outage?startDate=2023-01-01&endDate=2023-02-01"

    hdr ={
    # Request headers
    'Cache-Control': 'no-cache',
    'API-KEY': 'ff8bd8112f6942ac97bb08cc88d0deae',
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())
    print(response.read())
except Exception as e:
    print(e)
####################################