import os

ProductionConfig = {
    "ENV": "production",
    "DEBUG": False,
    "SECRET_KEY": os.environ.get('SECRET_KEY'),
    "SOME_API_KEY_1": os.environ.get("SOME_API_KEY_1"),
    "SOME_API_KEY_2": os.environ.get("SOME_API_KEY_2"),
}

DevelopmentConfig = {
    "ENV": "development",
    "DEBUG": True,
    "SECRET_KEY": os.environ.get('SECRET_KEY'),
    "SOME_API_KEY_1": os.environ.get("DEV_SOME_API_KEY_1"),
    "SOME_API_KEY_2": os.environ.get("DEV_SOME_API_KEY_2"),
}