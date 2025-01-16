from agents.navigation import NavigationAgent
from api.here import HereAPI
from models.mistral import MistralModel
from tools.autosuggest_tool import AutosuggestTool
from tools.discover_tool import DiscoverTool
from tools.geocode_tool import GeocodeTool
from tools.route_tool import RouteTool
from os import getenv


model_path = getenv('MODEL_PATH', '/app/models/Mistral-7B-Instruct-v0.3.Q8_0.gguf')
class NavigationApp:
    def __init__(self, model_path: str):
        model = MistralModel(model_path)
        here_api = HereAPI()
        geocode_tool = GeocodeTool(api=here_api)
        route_tool = RouteTool(api=here_api)
        discover_tool = DiscoverTool(api=here_api)
        autosuggest_tool = AutosuggestTool(api=here_api)
        self.agent = NavigationAgent(
            model.get_llm(),
            geocode_tool,
            route_tool,
            discover_tool,
            autosuggest_tool
        )

    def process_query(self, query: str):
        result = self.agent.run(query)
        if result.action == "geocode" and result.geocoding_result:
            return f"Geocoding result for '{result.geocoding_result.address}':\n" \
                   f"Latitude: {result.geocoding_result.latitude}\n" \
                   f"Longitude: {result.geocoding_result.longitude}\n\n" \
                   f"Raw response: {result.raw_response}"
        elif result.action == "route" and result.routing_result:
            return f"Route from '{result.routing_result.origin}' to '{result.routing_result.destination}':\n" \
                   f"Distance: {result.routing_result.distance_km:.2f} km\n" \
                   f"Estimated duration: {result.routing_result.duration_hours:.2f} hours\n\n" \
                   f"Raw response: {result.raw_response}"
        elif result.action == "discover" and result.discover_result:
            return f"Discover results for '{result.discover_result.query}':\n" \
                   f"{result.discover_result.results}\n\n" \
                   f"Raw response: {result.raw_response}"
        elif result.action == "autosuggest" and result.autosuggest_result:
            return f"Autosuggest results for '{result.autosuggest_result.query}':\n" \
                   f"{result.autosuggest_result.suggestions}\n\n" \
                   f"Raw response: {result.raw_response}"
        else:
            return f"Error or unexpected result: {result.raw_response}"
