import os
import flaskapp.errors as errors
from flask import Flask, jsonify, request
from flask_cors import CORS #, cross_origin

from flaskapp.resources.heretraffic import HERETraffic
from flaskapp.resources.utils import coordinates_are_valid
from flaskapp.config import get_config
from flaskapp.road import get_road_data

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
with open(os.environ.get("ALLOWED_ORIGINS_PATH"), 'r') as f:
    origins = [line.strip() for line in f.readlines()]
cors = CORS(app, resources={r"/api/*": {"origins": origins}})
app.config.update(get_config())


# Query should look like the following:
# ?ul=lat,long?br=lat,long 
@app.route('/api/v1/bbox')
def bbox():
    args = request.args
    if "ul" not in args or "br" not in args:
        return generate_error_response(errors.INVALID_SYNTAX, 'Missing either "ul" or "br" argument'), 400
    upper_left_string = args["ul"]
    bottom_right_string = args["br"]
    if not valid_coordinate_format(upper_left_string) or not valid_coordinate_format(bottom_right_string):
        return generate_error_response(errors.INVALID_SYNTAX, 'Query must follow the form "ul=lat,long&br=lat,long", where lat and long are floating point numbers.'), 400
    upper_left = get_coordinates(upper_left_string)   
    bottom_right = get_coordinates(bottom_right_string)
    if upper_left is None or bottom_right is None:
        return generate_error_response(errors.INVALID_COORDINATES, "Latitude must be >= -90 and <= 90, longitude must be >= -180 and <= 180"), 400
    
    # TODO Temporary code. Must calculate emission data. Likely in a seperate module.
    here = HERETraffic(app.config["HERE_TRAFFIC_API_KEY"])
    code, response = here.get_flow_data(upper_left, bottom_right)
    if code == 200:
        roads = get_road_data(response)
        response = []
        for road in roads:
            segments = []
            for segment in road.segments:
                segments.append({
                    "NOx": 0,
                    "VOC": 0,
                    "PM2.5": 0,
                    "PM10": 0,
                    "CO2": segment.jam_factor,   # Like I said, temporary code :)
                    "shape": segment.shape
                })
            emission_data = {
                "road": road.name,
                "segments": segments
            }
            response.append(emission_data)
        return jsonify(response), 200
    else:
        return f"Looks like HERE isn't happy. Response code: {code}", 500

def valid_coordinate_format(coordinate_string):
    try:
        lat_str, long_str = coordinate_string.split(",")
        float(lat_str)
        float(long_str)
    except ValueError:
        return False
    return True

def get_coordinates(coordinate_string):
    lat_str, long_str = coordinate_string.split(",")
    coords = ( float(lat_str), float(long_str) )
    if coordinates_are_valid(coords):
        return (float(lat_str), float(long_str))
    else:
        return None

def generate_error_response(name, description):
    return jsonify(
        {
            "name": name,
            "description": description
        }
    )