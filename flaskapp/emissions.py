from flaskapp.road import RoadType, Unit

class SegmentEmissions:
    def __init__(self):
        self.co = 0
        self.co2 = 0
        self.nox = 0
        self.pm25 = 0

CO_AVG_GRAMS_PER_MILE_PER_CAR = 4.152
CO2_AVG_GRAMS_PER_MILE_PER_CAR = 404.0
NOX_AVG_GRAMS_PER_MILE_PER_CAR = 0.192
PM2_5_AVG_GRAMS_PER_MILE_PER_CAR = 0.008 

# Level of service categories. Numbers represent personal car per mile per lane (PC/mi/Ln)
LOS_A_RANGE = (6, 11)   # Best case. No, we never assume a road has 0 cars at any time.
LOS_B_RANGE = (11, 18)  # HERE doesn't provide enough information about quiet roads for that to be a good assumption.
LOS_C_RANGE = (18, 26)
LOS_D_RANGE = (26, 35)
LOS_E_RANGE = (35, 200)

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
        normalized = jam_factor / 2 
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
    e.co = personal_cars * CO_AVG_GRAMS_PER_MILE_PER_CAR 
    e.co2 = personal_cars * CO2_AVG_GRAMS_PER_MILE_PER_CAR 
    e.nox = personal_cars * NOX_AVG_GRAMS_PER_MILE_PER_CAR 
    e.pm25 = personal_cars * PM2_5_AVG_GRAMS_PER_MILE_PER_CAR 
    return e

def model_road_emissions(roads):
    data = []
    for road in roads:
        emissions = []
        for segment in road.segments:
            segment_emissions = calculate_segment_emissions(segment)
            emissions.append({
                "CO": segment_emissions.co,
                "CO2": segment_emissions.co2,
                "NOx": segment_emissions.nox,
                "PM2.5": segment_emissions.pm25,
                "shape": segment.shape
            })
        data.append({
            "road": road.name,
            "segments": emissions
        })
    return data

