def find_massht(json_response):
    top_delta = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]["boundedBy"]["Envelope"]
    x1, y1 = map(float, top_delta["lowerCorner"].split())
    x2, y2 = map(float, top_delta["upperCorner"].split())
    return [abs(x1 - x2), abs(y1 - y2)]
