# backend

## Developing

1) Install pipenv
2) Navigate to root project directory
3) `pipenv shell`
4) `pipenv install`
5) `export FLASK_APP=flaskapp/app.py`
6) `export FLASK_ENV=development`
7) `export DEV_HERE_TRAFFIC_API_KEY=your_api_key`
8) `flask run`

Optionally, you may create a new file in the root project directory named `.env` like below. Any time `flask run` is executed, it'll automatically export these variables.
```
FLASK_APP=flaskapp/app.py
FLASK_ENV=development
DEV_HERE_TRAFFIC_API_KEY=your_api_key
```

You should now be able to reach the backend service on [http://localhost:5000](http://localhost:5000)
