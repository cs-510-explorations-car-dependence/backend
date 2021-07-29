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
    raise_if_invalid_coordinates(upperleftbb)
    raise_if_invalid_coordinates(lowerrightbb)
    url = build_url(upperleftbb, lowerrightbb)
    response = requests.get(url)
    # TODO Convert to something usable

def build_url(upperleftbb, lowerrightbb):
    return (
        "https://overpass-api.de/api/interpreter?data="
        "("
            f"way({upperleftbb[0]},{upperleftbb[1]},{lowerrightbb[0]},{lowerrightbb[1]})"
                f"{WAY_FILTERS};"
            f"<;"
        "); out meta;"
    )

