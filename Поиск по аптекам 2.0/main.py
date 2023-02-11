import requests
import sys
from PIL import Image
from io import BytesIO
from dist import lonlat_distance


def main():
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    toponym_to_find = " ".join(sys.argv[1:])
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('error')

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": f'{toponym_longitude},{toponym_lattitude}',
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        print(1)
        print('Аптек поблизости не найдено')
        print(response.reason)
        return

    json_response = response.json()
    try:
        organization = json_response["features"][0]
    except Exception:
        print('Аптек поблизости не найдено')
        return
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])

    map_params = {
        "ll": f'{toponym_longitude},{toponym_lattitude}',
        "l": "map",
        "pt": "{0},pm2bm~{1},pm2am".format(org_point, f'{toponym_longitude},{toponym_lattitude}')
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(
        response.content)).show()
    print('=============================')
    print(f'АДРЕС АПТЕКИ: {org_address}')
    print(f'ВРЕМЯ РАБОТЫ: {organization["properties"]["CompanyMetaData"]["Hours"]["text"]}')
    print(f'РАССТОЯНИЕ ОТ ТОЧКИ А: {round(lonlat_distance(tuple(map(float, (toponym_longitude, toponym_lattitude))), tuple(map(float, org_point.split(",")))) / 1000, 3)}км')
    print('=============================')


main()
