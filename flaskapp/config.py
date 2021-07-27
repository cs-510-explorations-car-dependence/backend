import os
from dotenv import load_dotenv

def get_config():
    load_dotenv()
    dev_mode = os.environ.get("DEBUG").lower() == "yes"
    return {
        "ENV": "development" if dev_mode else "production",
        "DEBUG": dev_mode,
        "SECRET_KEY": os.environ.get('SECRET_KEY'),
        "HERE_TRAFFIC_API_KEY": os.environ.get("HERE_TRAFFIC_API_KEY") if not dev_mode else os.environ.get("DEV_HERE_TRAFFIC_API_KEY"),
        "OVERPASS_API_KEY_2": os.environ.get("OVERPASS_API_KEY") if not dev_mode else os.environ.get("DEV_OVERPASS_API_KEY"),
    }