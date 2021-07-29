import requests
from flaskapp.resources.utils import raise_if_invalid_coordinates

# https://wiki.openstreetmap.org/wiki/Key:highway
WAY_FILTERS = (
                """["highway"]"""
                """["highway"!="motorway_link"]"""
                """["highway"!="trunk_link"]"""
                """["highway"!="primary_link"]"""
                """["highway"!="secondary_link"]"""
                """["highway"!="tertiary_link"]"""
                """["highway"!="service"]"""
                """["highway"!="pedestrian"]"""
                """["highway"!="track"]"""
                """["highway"!="bus_guideway"]"""
                """["highway"!="escape"]"""
                """["highway"!="raceway"]"""
                """["highway"!="footway"]"""
                """["highway"!="bridleway"]"""
                """["highway"!="steps"]"""
                """["highway"!="corridor"]"""
                """["highway"!="path"]"""
                """["highway"!="cycleway"]"""
                """["highway"!="proposed"]"""
                """["highway"!="construction"]"""
              )

def get_road_data(upperleftbb, lowerrightbb):
    """
    Gets information about all highways found within the bounding box.
    Both arguments are a (float latitude, float longitude) pair representing either the upper left or the bottom
    right coordinate of the bounding box to be searched.
    Returns a (int status_code, dict json_response) pair. If status_code is not 200, then json_response will be empty.
    """
    raise_if_invalid_coordinates(upperleftbb)
    raise_if_invalid_coordinates(lowerrightbb)
    url = build_url(upperleftbb, lowerrightbb)
    response = requests.get(url)
    if response.status_code == 200:
        return 200, response.json()
    return response.status_code, {}

def build_url(upperleftbb, lowerrightbb):
    return (
        "https://overpass-api.de/api/interpreter?data=[out:json];"
        "("
            f"way({upperleftbb[0]},{upperleftbb[1]},{lowerrightbb[0]},{lowerrightbb[1]})"
                f"{WAY_FILTERS};"
            f"<;"
        "); out meta;"
    )
