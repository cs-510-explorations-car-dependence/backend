from flaskapp.road import RoadType, Unit

class SegmentEmissions:
    def __init__(self):
        self.co2 = 0
        self.nox = 0
        self.pm25 = 0

# Average emissions for personal cars. Numbers represent grams per mile (g/mi)
CO2_AVG_EMISSIONS = 404.0
NOX_AVG_EMISSIONS = 0.192
PM2_5_AVG_EMISSIONS = 0.008 
# TODO Missing a few.

# Level of service categories. Numbers represent personal car per mile per lane (PC/mi/Ln)
LOS_A = 11    # Best case (No, we never assume a road has 0 cars at any time.
LOS_B = 18    #            HERE doesn't provide enough information about quiet roads for that to be a good assumption.)
LOS_C = 26
LOS_D = 35
LOS_E = 45
LOS_F = 200   # Worst case

LOS_A_RANGE = (LOS_A, LOS_B)
LOS_B_RANGE = (LOS_B, LOS_C)
LOS_C_RANGE = (LOS_C, LOS_D)
LOS_D_RANGE = (LOS_D, LOS_E)
LOS_E_RANGE = (LOS_E, LOS_F)

# Lanes per direction. (So, a total of 10 lanes if MOTORWAY goes in both directions)
lanes = {
    RoadType.MOTORWAY: 4.25, # Usually varies between 3 to 5 lanes, but not uncommon to see 5+, so it's biased a bit towards 5
    RoadType.TRUNK: 3,
    RoadType.PRIMARY: 2,
    RoadType.UNCLASSIFIED: 1,
    RoadType.RESIDENTIAL: 1
}


def calculate_segment_emissions(segment):
    e = SegmentEmissions()
    if segment.closed:
        return e   # Everything is zeroed out 
    jam_factor = segment.jam_factor
    if jam_factor >= 0 and jam_factor <= 2:
        range = LOS_A_RANGE
        normalized = jam_factor / 2 if jam_factor != 0 else 0.0000001   # Prevents divide by zero later.
    elif jam_factor > 2 and jam_factor <= 4:
        range = LOS_B_RANGE
        normalized = (jam_factor - 2) / 2
    elif jam_factor > 4 and jam_factor <= 6:
        range = LOS_C_RANGE
        normalized = (jam_factor - 4) / 2
    elif jam_factor > 6 and jam_factor <= 8:
        range = LOS_D_RANGE
        normalized = (jam_factor - 6) / 2
    else:  # Must be between 8 and 10
        range = LOS_E_RANGE
        normalized = (jam_factor - 8) / 2
    # normalized represents "how far" a number is from the lower to the upper bound of its category.
    # For example, 5.68 maps to the 4 thru 6 category, so normalized is 0.84 since 5.68 is 84% of the way from 4 to 6.
    lower_limit, upper_limit = range
    pc_per_mile_per_lane = (upper_limit - lower_limit) * normalized + lower_limit

    length_in_miles = segment.length * 0.621371 if segment.length_unit is Unit.METRIC else segment.length
    personal_cars = pc_per_mile_per_lane * lanes[segment.type] * length_in_miles
    e.co2 = personal_cars * CO2_AVG_EMISSIONS
    e.nox = personal_cars * NOX_AVG_EMISSIONS
    e.pm25 = personal_cars * PM2_5_AVG_EMISSIONS
    return e

def model_road_emissions(roads):
    data = []
    for road in roads:
        emissions = []
        for segment in road.segments:
            segment_emissions = calculate_segment_emissions(segment)
            emissions.append({
                "NOx": segment_emissions.nox,
                "CO2": segment_emissions.co2,
                "PM2.5": segment_emissions.pm25,
                "PM10": 0,  #TODO Missing
                "VOC": 0,  # TODO Missing
                "shape": segment.shape
            })
        data.append({
            "road": road.name,
            "segments": emissions
        })
    return data
