import pytest
import json
from flaskapp.app import app
from flaskapp import errors

@pytest.fixture
def client():
    app.config.update({"TESTING": True})
    with app.test_client() as client:
        yield client

def test_v1_bbox_valid_input(client):
    response = client.get('/api/v1/bbox?ul=34.44855,-118.638192&br=34.487186,-118.594933')
    assert response.status_code == 200

def test_v1_bbox_missing_input(client):
    response = client.get('/api/v1/bbox')
    assert response.status_code == 400
    data = json.loads(response.data.decode("utf-8"))
    assert data["name"] == errors.INVALID_SYNTAX

def test_v1_bbox_bad_query(client):
    response = client.get('/api/v1/bbox?br=1234.44855,-118.638192&br=34.487186,-118.594933')
    assert response.status_code == 400
    data = json.loads(response.data.decode("utf-8"))
    assert data["name"] == errors.INVALID_SYNTAX

def test_v1_bbox_bad_coordinates(client):
    response = client.get('/api/v1/bbox?ul=1234.44855,-118.638192&br=34.487186,-118.594933')
    assert response.status_code == 400
    data = json.loads(response.data.decode("utf-8"))
    assert data["name"] == errors.INVALID_COORDINATES