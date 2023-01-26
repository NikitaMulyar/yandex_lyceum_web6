import requests
import sys
from PIL import Image
from io import BytesIO


search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

address_ll = sys.argv[1]

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    print('error')


json_response = response.json()

map_params = {"ll": address_ll,
              "l": "map",
              "pt": []
              }
for i in json_response["features"]:
    organization = i
    org_hours = organization["properties"]["CompanyMetaData"]
    if "Hours" not in org_hours:
        org_hours = "None"
    else:
        org_hours = org_hours["Hours"]["text"]
    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])

    res = ''
    if org_hours == 'круглосуточно':
        res = 'pm2dgm'
    elif org_hours == 'None':
        res = 'pm2grm'
    else:
        res = 'pm2dbm'
    map_params["pt"].append("{0},{1}".format(org_point, res))

map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params["pt"] = "~".join(map_params["pt"])
print(map_params)
response = requests.get(map_api_server, params=map_params)
print(response.content)

Image.open(BytesIO(
    response.content)).show()
