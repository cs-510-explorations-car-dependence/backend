import requests
from flaskapp.resources.utils import raise_if_invalid_coordinates

class HERETraffic:
	""" A thin wrapper over the HERE Traffic Flow API. """
	def __init__(self, apikey):
		self.apikey = apikey
		self.url_base = f"https://traffic.ls.hereapi.com/traffic/6.2/flow.json?apiKey={apikey}&responseattributes=sh,fc"

	def get_flow_data(self, upperleftbb, lowerrightbb):
		"""
		Gets raw Road Shape and Road Class Filter response. 
		An example output is found here: https://developer.here.com/documentation/traffic/dev_guide/topics_v6.1/example-flow-sh-frc.html
		Both arguments are a (float latitude, float longitude) pair representing either the upper left or the bottom
		right coordinate of the bounding box to be searched.
		Returns a (int status_code, dict json_response) pair. If status_code is not 200, then json_response will be empty.
		"""
		raise_if_invalid_coordinates(upperleftbb)
		raise_if_invalid_coordinates(lowerrightbb)
		request_url = f"{self.url_base}&bbox={upperleftbb[0]},{upperleftbb[1]};{lowerrightbb[0]},{lowerrightbb[1]}"
		response = requests.get(request_url)
		if response.status_code == 200:
			return 200, response.json()
		return response.status_code, {}
	