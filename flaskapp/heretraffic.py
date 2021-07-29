import requests

class InvalidCoordinates(BaseException):
	pass

class HERETraffic:
	""" A thin wrapper over the HERE Traffic Flow API. """
	def __init__(self, apikey):
		self.apikey = apikey
		self.url_base = f"https://traffic.ls.hereapi.com/traffic/6.2/flow.json?apiKey={apikey}&responseattributes=sh,fc"

	def get_flow_data(self, upperleftbb, lowerrightbb):
		"""
		Gets raw Road Shape and Road Class Filter response. 
		https://developer.here.com/documentation/traffic/dev_guide/topics_v6.1/example-flow-sh-frc.html
		Both arguments are a (float latitude, float longitude) pair representing either the upper left or the bottom
		right coordinate of the bounding box to be searched.
		Returns a (int status_code, dict json_response) pair. If status_code is not 200, then json_response will be empty.
		"""
		self._raise_if_invalid_coordinates(upperleftbb)
		self._raise_if_invalid_coordinates(lowerrightbb)
		request_url = f"{self.url_base}&bbox={upperleftbb[0]},{upperleftbb[1]};{lowerrightbb[0]},{lowerrightbb[1]}"
		response = requests.get(request_url)
		if response.status_code == 200:
			return 200, response.json
		return response.status_code, {}
	
	@staticmethod
	def _raise_if_invalid_coordinates(lat_long_pair):
		lat = lat_long_pair[0]
		long = lat_long_pair[1]
		if lat < -90 or lat > 90:
			raise InvalidCoordinates(f"Latitude ({lat}) must be between -90 and 90 degrees")
		if lat < -180 or lat > 80:
			raise InvalidCoordinates(f"Longitude ({lat}) must be between -90 and 90 degrees")
