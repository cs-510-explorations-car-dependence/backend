from flaskapp.config import get_config
from flask import Flask, jsonify
from flask_cors import CORS #, cross_origin

app = Flask(__name__)
app.config.update(get_config())

@app.route('/api/route/')
def test_route():
    return jsonify({'route':[
      [45.5, -122.7],
      [45.49, -122.68],
      [45.52, -122.72],
      [45.5, -122.7],
    ]})
