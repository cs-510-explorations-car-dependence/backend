import os
import json
from flaskapp.road import get_road_data, Road

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")

def test_get_road_data():
    with open(os.path.join(SAMPLES_DIR, "here_flow_shape_portland.json")) as f:
        HERE_data = json.load(f)
        roads = get_road_data(HERE_data)
        assert len(roads) == 2

        nicolai = roads[0]
        mlk = roads[1]
        assert len(nicolai.segments) == 1
        assert len(mlk.segments) == 2

        assert len(nicolai.segments[0].shape) == 5
        assert nicolai.segments[0].jam_factor == 10.0
        assert nicolai.segments[0].closed == True