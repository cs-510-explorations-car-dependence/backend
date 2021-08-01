from enum import Enum
import Levenshtein

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

class Road:
    ASSUMED_LANECOUNT = 1   # The amount of lanes on a road to assume if information is not available
    """ Contains all significant data we care about in a road that can be aquired from resources. """
    def __init__(self):
        self.name = ""
        self.type = RoadType.UNKNOWN
        self.shape = []   # Array of Segments
        self.lane_count_positive = None  # Lanes going in one direction
        self.lane_count_negative = None  # Lanes going in the opposite direction

    def update_via_overpass_schema(self, way):
        """
        Parse a way type (from the Overpass JSON schema) and updates self based on what it finds.
        """
        tags = way["tags"]
        self.name = self.normalize_road_name(tags["name"]) if "name" in tags else ""
        self.type = RoadType(tags["highway"].upper()) if "highway" in tags else RoadType.UNKNOWN
        if "oneway" in tags and tags["oneway"] == "yes":
            self.lane_count_positive = tags["lanes:forward"] if "lanes:forward" in tags else 1
            self.lane_count_negative = 0
        else:
            self.lane_count_positive = tags["lanes:forward"] if "lanes:forward" in tags else Road.ASSUMED_LANECOUNT
            self.lane_count_negative = tags["lanes:forward"] if "lanes:forward" in tags else Road.ASSUMED_LANECOUNT

    def update_via_here_flow_item(self, here_fi):
        """
        Parses a flow item and updates the Road's segments with their current traffic flow.
        """
        # TODO Blocked. Awaiting to hear back from HERE Development Support. https://stackoverflow.com/questions/68582681/how-do-i-couple-segmented-cf-traffic-data-ss-with-shape-data-shp
        pass

    @staticmethod
    def normalize_road_name(name):
        """ Normalizes string: name by updating/removing characters deemed irrelevent for road name identification. """
        return name.strip().lower()

class Segment:
    def __init__(self):
        self.first_coord_pair = None  # (latitude, longitude) tuple
        self.second_coord_pair = None
        self.jam_factor = None
        self.segment_closed = False
        self.length = 0

def get_road_data(here_dict_response, overpass_dict_response):
    possible_roads = []
    returned_roads = []
    for obj in overpass_dict_response:
        # TODO This doesn't work. Overpass breaks roads up into multiple ways. Should have expected that.
        if obj["type"] == "way":
            new_road = Road()
            new_road.update_overpass_schema(obj)
            if new_road.name:
                possible_roads.append(new_road)
    for roadway in here_dict_response["RWS"]["RW"]:
        flow_item = roadway["FIS"][0]["FI"][0] # TODO In what scenario is there multiple FL (Flow items)? Shouldn't a roadway have one flow item with one name?
        name = flow_item["TMC"]["DE"].lower()
        road_to_update = _guess_road(name, possible_roads.values())
        if road_to_update is None:
            continue  # Road data wasn't in HERE response.
        road_to_update.update_via_here_flow_item(flow_item)
        returned_roads.append(road_to_update)
    return returned_roads

MINIMUM_JARO_SIMILARITY = 0.9
def _guess_road(name, roads):
    """
    Given a string: name and a list of Road, returns the Road in the list whose name is closest to the name argument.
    If no plausible Road exists, returns None.
    """
    comparison_name = Road.normalize_road_name(name)
    most_likely_road = None
    highest_similarity = 0
    for road in roads:
        if highest_similarity == 1:
            return most_likely_road
        other_name = road.name
        similarity = Levenshtein.jaro(comparison_name, other_name)
        if similarity > highest_similarity and similarity > MINIMUM_JARO_SIMILARITY:
            most_likely_road = road
    return most_likely_road
