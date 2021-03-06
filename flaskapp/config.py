import os

def get_config():
    dev_mode = os.environ.get("FLASK_ENV").lower() == "development"
    return {
        "SECRET_KEY": os.environ.get('SECRET_KEY'),
        "HERE_TRAFFIC_API_KEY": os.environ.get("HERE_TRAFFIC_API_KEY") if not dev_mode else os.environ.get("DEV_HERE_TRAFFIC_API_KEY"),
    }