########### Python 3.2 #############
import urllib.request, json

print('Hello')

try:
    url = "https://apimgw.aeso.ca/public/loadoutageforecast-api/v1/loadOutageReport?startDate=2013-12-22%20&endDate=2015-12-22%20"

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