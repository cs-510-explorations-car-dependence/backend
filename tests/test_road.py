import os
import json
from flaskapp.road import get_road_data, Road

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")

def test_get_road_data():
    with open(os.path.join(SAMPLES_DIR, "here_flow_shape_portland.json")) as f:
        HERE_data = json.load(f)
        roads = get_road_data(HERE_data)
        assert roads == 2