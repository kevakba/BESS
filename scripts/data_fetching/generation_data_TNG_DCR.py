import urllib.request, json

try:
    url = "https://apimgw.aeso.ca/public/currentsupplydemand-api/v1/csd/generation/assets/current"

    hdr ={
    # Request headers
    'Cache-Control': 'no-cache',
    'API-KEY': '*************',
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    print(response.getcode())
    print(response.read())
except Exception as e:
    print(e)
