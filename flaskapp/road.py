from enum import Enum

# Based on https://wiki.openstreetmap.org/wiki/Key:highway
class RoadType(Enum):
    MOTORWAY = 0
    TRUNK = 1
    PRIMARY = 2
    SECONDARY = 3
    TERTIARY = 4
    UNCLASSIFIED = 5   # Not equivalent to UNKOWN. This name is a historical artifact of the UK road naming system
    RESIDENTIAL = 6
    LIVING_STREET = 7
    BUSWAY = 8
    ROAD = 9
    UNKNOWN = 9        # Yes, "Road" is equivalent to "Unknown"

class Unit(Enum):
    METRIC = 0
    IMPERIAL = 1

class Direction(Enum):
    POSITIVE = 0
    NEGATIVE = 1

class Road:

    """ Contains all significant data we care about in a road that can be aquired from resources. """
    def __init__(self, length_unit):
        self.name = ""
        self.segments = []
        self.length_unit = length_unit

    # Each flow item is a segment of a Road.
    def add_flow_item(self, here_fi):
        """
        Parses a flow item and updates the Road's segments with their current traffic flow.
        """
        self.name = here_fi["TMC"]["DE"]
        flow_info = here_fi["CF"][0]  # I've never seen more than a single "CF" object. We will assume the first.
        if flow_info["JF"] == -1:   # Without knowing the jam factor, we have no clue how jammed the road is. Ignored.
            return
        segment = Segment(self.length_unit)
        segment.update_via_here_flow_item(here_fi)
        self.segments.append(segment)

class Segment:
    def __init__(self, length_unit):
        self.type = RoadType.UNKNOWN
        self.direction = None
        self.shape = []  # Array of (latitude, longitude tuple)
        self.jam_factor = None   # Float ranging from 0 to 10, as defined by HERE
        self.closed = False
        self.length_unit = length_unit  # Describes whether flow items are metric or imperial
        self.length = 0

    def update_via_here_flow_item(self, here_fi):
        function_class_count = {   # Each SHP has a function class, indicating road type. Each segment's type is 
            1: 0,                  # defined as the most common function class that occured in HERE's SHP data.
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }
        for SHP in here_fi["SHP"]:
            function_class = SHP["FC"]
            function_class_count[function_class] += 1
            for value in SHP["value"]:  # I've never seen a "value" array hold more than one string, but playing it safe
                for coordinate_string in value.strip().split(" "):
                    coordinates = self._get_lat_long_from_string(coordinate_string)
                    self.shape.append(coordinates)
        function_class = max(function_class_count, key=function_class_count.get)
        self.type = self.convert_function_class_to_roadtype(function_class)

        # HERE sometimes splits flow data into even finer segments within an "SSS" object inside the "CF" object.
        # We disregard these finer segments, since there's no way to correlate said data to the shape data found above.
        flow_info = here_fi["CF"][0]  # I've never seen more than a single "CF" object. We will assume the first.
        self.jam_factor = flow_info["JF"]
        self.closed = self.jam_factor == 10
        length = here_fi["TMC"]["LE"]
        self.length = length * 0.621371 if self.length_unit is Unit.METRIC else length
        self.direction = Direction.POSITIVE if here_fi["TMC"]["QD"] == "+" else Direction.NEGATIVE

    @staticmethod
    def _get_lat_long_from_string(string):
        lat_str, long_str = string.split(",")
        return (float(lat_str), float(long_str))

    @staticmethod
    def convert_function_class_to_roadtype(function_class):
        # Values loosely defined at https://developer.here.com/documentation/routing/dev_guide/topics/resource-type-functional-class.html
        if function_class == 1:     # Equivalent to some parts of CA-126 https://www.google.com/maps/place/34%C2%B027'11.1%22N+118%C2%B036'56.3%22W
            return RoadType.MOTORWAY
        elif function_class == 2:   # Equivalent to some parts of I-5  https://www.google.com/maps/place/45%C2%B035'11.0%22N+122%C2%B040'48.2%22W 
            return RoadType.TRUNK
        elif function_class == 3:   # Equivalent to NE Columbia Blvd, Portland OR
            return RoadType.PRIMARY
        elif function_class == 4:   # Equivalent to N Chautauqua Blvd, Portland OR
            return RoadType.UNCLASSIFIED
        else:  # function_class == 5. Equivalent to N Willamette Blvd, Portland OR
            return RoadType.RESIDENTIAL
        

def get_road_data(here_dict_response):
    roads = {}
    unit = Unit.METRIC if here_dict_response["UNITS"] == "metric" else Unit.IMPERIAL
    for RWS_obj in here_dict_response["RWS"]:  # I've never seen RWS hold more than one object, but playing it safe
        for roadway in RWS_obj["RW"]:
            for FIS_obj in roadway["FIS"]:   # I have never seen FIS hold more than one object, but playing it safe
                for flow_item in FIS_obj["FI"]:
                    name = flow_item["TMC"]["DE"]
                    if name in roads:
                        road = roads[name]
                    else:
                        road = Road(unit)
                        roads[name] = road
                    road.add_flow_item(flow_item)
    return list(roads.values())
