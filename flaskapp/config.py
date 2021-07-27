import os

ProductionConfig = {
    "ENV": "production",
    "DEBUG": False,
    "SECRET_KEY": os.environ.get('SECRET_KEY'),
    "HERE_TRAFFIC_API_KEY": os.environ.get("HERE_TRAFFIC_API_KEY"),
    "OVERPASS_API_KEY_2": os.environ.get("OVERPASS_API_KEY"),
}

DevelopmentConfig = {
    "ENV": "development",
    "DEBUG": True,
    "SECRET_KEY": os.environ.get('SECRET_KEY'),
    "HERE_TRAFFIC_API_KEY": os.environ.get("DEV_HERE_TRAFFIC_API_KEY"),
    "OVERPASS_API_KEY_2": os.environ.get("DEV_OVERPASS_API_KEY"),
}