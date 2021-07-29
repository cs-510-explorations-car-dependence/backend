import enum

# Based on https://wiki.openstreetmap.org/wiki/Key:highway
class RoadType(enum):
    UNDEFINED = 0      # Used when we don't even know if it's an unknown road.
    MOTORWAY = 1
    PRIMARY = 2
    SECONDARY = 3
    TERTIARY = 4
    UNCLASSIFIED = 5   # Not equivalent to UNKOWN. This name is a historical artifact of the UK road naming system
    RESIDENTIAL = 6
    LIVINGSTREET = 7
    BUSWAY = 8
    ROAD = 9
    UNKNOWN = 9        # Yes, "Road" is equivalent to "Unknown"

class Road:
    def __init__(self):
        self.name = ""
        self.type = RoadType.UNDEFINED
        self.shape = []   # 2D array of coordinate pairs

def get_road_data(here_json_response, overpass_xml_response):
    """ 
    Given a json response from resources.heretraffic.HERETraffic.get_road_data, 
    and an xml response from resources.overpass.get_road_data, returns a list of Road.
    """
    pass