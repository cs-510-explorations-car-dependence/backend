import os
from dotenv import load_dotenv
from flaskapp.config import get_config
from flask import Flask, jsonify
from flask_cors import CORS #, cross_origin

load_dotenv()
app = Flask(__name__)
with open(os.environ.get("ALLOWED_ORIGINS_PATH"), 'r') as f:
    origins = [line.strip() for line in f.readlines()]
cors = CORS(app, resources={r"/api/*": {"origins": origins}})
app.config.update(get_config())

@app.route('/api/route/')
def test_route():
    return jsonify({'route':[
      [45.5, -122.7],
      [45.49, -122.68],
      [45.52, -122.72],
      [45.5, -122.7],
    ]})
