import requests
import sys
from PIL import Image
from io import BytesIO
from dist import lonlat_distance


def main():
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    crs = sys.argv[1:]
    if type(crs) == str:
        address_ll = crs
    else:
        address_ll = ",".join([i.strip(',') for i in crs])

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
        "ll": address_ll,
        "l": "map",
        "pt": "{0},pm2bm~{1},pm2am".format(org_point, address_ll)
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(
        response.content)).show()
    print('=============================')
    print(f'АДРЕС АПТЕКИ: {org_address}')
    print(f'ВРЕМЯ РАБОТЫ: {organization["properties"]["CompanyMetaData"]["Hours"]["text"]}')
    print(f'РАССТОЯНИЕ ОТ ТОЧКИ А: {round(lonlat_distance(tuple(map(float, address_ll.split(","))), tuple(map(float, org_point.split(",")))) / 1000, 3)}км')
    print('=============================')


main()
