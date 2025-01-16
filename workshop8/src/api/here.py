import requests
from typing import Dict, Any
from utils.config import Config


class HereAPI:
    def __init__(self):
        self.api_key = "API_KEY"
        self.geocode_url = "https://geocode.search.hereapi.com/v1/geocode"
        self.route_url = "https://router.hereapi.com/v8/routes"
        self.discover_url = "https://discover.search.hereapi.com/v1/discover"
        self.autosuggest_url = "https://autosuggest.search.hereapi.com/v1/autosuggest"

    def geocode(self, address: str) -> Dict[str, Any]:
        params = {
            "q": address,
            "apiKey": self.api_key
        }
        response = requests.get(self.geocode_url, params=params)
        return response.json()

    def calculate_route(self, origin: str, destination: str) -> Dict[str, Any]:
        params = {
            "transportMode": "car",
            "origin": origin,
            "destination": destination,
            "return": "summary",
            "apiKey": self.api_key
        }
        response = requests.get(self.route_url, params=params)
        return response.json()

    def discover(self, query: str, at: str = None, limit: int = 20) -> Dict[str, Any]:

        params = {
            "q": query,
            "limit": limit,
            "apiKey": self.api_key
        }
        if at:
            params["at"] = at
        response = requests.get(self.discover_url, params=params)
        return response.json()

    def autosuggest(self, query: str, at: str = None, limit: int = 20) -> Dict[str, Any]:
        params = {
            "q": query,
            "limit": limit,
            "apiKey": self.api_key
        }
        if at:
            params["at"] = at
        response = requests.get(self.autosuggest_url, params=params)
        return response.json()
