import requests
import sys
from PIL import Image
from io import BytesIO


def coords_of_address(address):
    try:
        res = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}&format=json')
        i = ','.join(res.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
            'Point']['pos'].split())
        return i
    except Exception:
        return None


def main():
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    address_ll = coords_of_address(sys.argv[1:])
    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print('Аптек поблизости не найдено')
        return

    json_response = response.json()
    map_params = {"ll": address_ll,
                  "l": "map",
                  "pt": []
                  }
    try:
        if not json_response["features"]:
            raise Exception
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
            if 'круглосуточно' in org_hours:
                res = 'pm2dgm'
            elif org_hours == 'None':
                res = 'pm2grm'
            else:
                res = 'pm2dbm'
            map_params["pt"].append("{0},{1}".format(org_point, res))
    except Exception:
        print('Аптек поблизости не найдено')
        return
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params["pt"] = "~".join(map_params["pt"])
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(
        response.content)).show()


main()
