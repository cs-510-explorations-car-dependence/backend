class InvalidCoordinates(BaseException):
	pass

def raise_if_invalid_coordinates(lat_long_pair):
	lat = lat_long_pair[0]
	long = lat_long_pair[1]
	if lat < -90 or lat > 90:
		raise InvalidCoordinates(f"Latitude ({lat}) must be between -90 and 90 degrees")
	if long < -180 or long > 180:
		raise InvalidCoordinates(f"Longitude ({long}) must be between -90 and 90 degrees")

def coordinates_are_valid(lat_long_pair):
	try:
		raise_if_invalid_coordinates(lat_long_pair)
		return True
	except InvalidCoordinates:
		return False
