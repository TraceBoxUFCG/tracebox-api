import requests

from app.common.core.env import GOOGLE_API_ADDRESS_KEY


class GoogleClient:
    def __init__(self):
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.auth = GOOGLE_API_ADDRESS_KEY

    def get_location_coordinates(self, location: str):
        response = requests.get(
            self.base_url, params={"key": self.auth, "address": location}
        ).json()["results"]

        address = response[0]
        location = address["geometry"]["location"]

        latitude = location["lat"]
        longitude = location["lng"]

        return (latitude, longitude)
