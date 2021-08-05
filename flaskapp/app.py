import os
import flaskapp.errors as errors
from flask import Flask, jsonify, request
from flask_cors import CORS #, cross_origin

from flaskapp.resources.heretraffic import HERETraffic
from flaskapp.resources.utils import coordinates_are_valid
from flaskapp.config import get_config
from flaskapp.road import get_road_data
from flaskapp.emissions import model_road_emissions

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
here = HERETraffic(app.config["HERE_TRAFFIC_API_KEY"])


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
    area = calculate_coordinate_area(upper_left, bottom_right)
    if area > 8000:
        return generate_error_response(errors.BBOX_TOO_LARGE, "Area of bounding box is too large.")
    
    code, response = here.get_flow_data(upper_left, bottom_right)
    if code == 200:
        roads = get_road_data(response)
        model = model_road_emissions(roads)
        return jsonify(model), 200
    else:
        return f"Looks like HERE isn't happy. Response code: {code}", 500  # TODO HERE Error handling

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

DIST_BETWEEN_LAT = 68.939
DIST_BETWEEN_LONG = 54.583
def calculate_coordinate_area(upper_left, bottom_right):
    """ Approximates the surface area (in square miles) of coordinates.  """
    x1, y1 = upper_left
    x2, y2 = bottom_right
    x1 += 90   # Translate everything out of the negative range. We only care about distance between points.
    x2 += 90
    y1 += 180 
    y2 += 180 
    return (abs(x1 - x2) * DIST_BETWEEN_LONG) * (abs(y1 - y2) * DIST_BETWEEN_LAT)

def generate_error_response(name, description):
    return jsonify(
        {
            "name": name,
            "description": description
        }
    )