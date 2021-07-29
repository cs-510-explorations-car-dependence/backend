import requests
from flaskapp.resources.utils import raise_if_invalid_coordinates

WAY_FILTERS = (
                """["highway"]"""
                """["v"!="footway"]"""
                """["v"!="path"]"""
                """["v"!="pedestrian"]"""
              )

def get_road_data(upperleftbb, lowerrightbb):
    raise_if_invalid_coordinates(upperleftbb)
    raise_if_invalid_coordinates(lowerrightbb)
    url = build_url(upperleftbb, lowerrightbb)
    response = requests.get(url)

def build_url(upperleftbb, lowerrightbb):
    return (
        "https://overpass-api.de/api/interpreter?data="
        "("
            f"way({upperleftbb[0]},{upperleftbb[1]},{lowerrightbb[0]},{lowerrightbb[1]})"
                f"{WAY_FILTERS};"
            f"<;"
        "); out meta;"
    )

