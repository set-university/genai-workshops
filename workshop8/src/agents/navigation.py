from utils.prompt import SYSTEM_PROMPT
import yaml
import re
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, Tuple, Dict


class GeocodingResult(BaseModel):
    address: str
    latitude: float
    longitude: float


class RoutingResult(BaseModel):
    origin: str
    destination: str
    distance_km: float
    duration_hours: float


class DiscoverResult(BaseModel):
    query: str
    results: str


class AutosuggestResult(BaseModel):
    query: str
    suggestions: str


class NavigationResult(BaseModel):
    action: str = Field(..., description="The action performed: 'geocode', 'route', 'discover', or 'autosuggest'")
    geocoding_result: Optional[GeocodingResult] = None
    routing_result: Optional[RoutingResult] = None
    discover_result: Optional[DiscoverResult] = None
    autosuggest_result: Optional[AutosuggestResult] = None
    raw_response: str = Field(..., description="The raw response from the model")


class NavigationAgent:
    def __init__(self, llm, geocode_tool, route_tool, discover_tool, autosuggest_tool):
        self.llm = llm
        self.geocode_tool = geocode_tool
        self.route_tool = route_tool
        self.discover_tool = discover_tool
        self.autosuggest_tool = autosuggest_tool
        self.output_parser = PydanticOutputParser(pydantic_object=NavigationResult)

        self.prompt = PromptTemplate(
            template=SYSTEM_PROMPT + "\n\nUser query: {query}\n\nResponse:",
            input_variables=["query"]
        )

    def run(self, query: str):
        try:
            _input = self.prompt.format(query=query)
            raw_output = self.llm.invoke(_input)

            action, params = self._parse_raw_output(raw_output)

            if action == "geocode":
                tool_result = self.geocode_tool._run({"address": params["address"]})
                lat, lon = self._extract_coordinates(tool_result)
                result = NavigationResult(
                    action="geocode",
                    geocoding_result=GeocodingResult(address=params["address"], latitude=lat, longitude=lon),
                    raw_response=raw_output
                )
            elif action == "route":
                origin_geocode = self.geocode_tool.run(params["origin"])
                destination_geocode = self.geocode_tool.run(params["destination"])

                origin_lat, origin_lon = self._extract_coordinates(origin_geocode)
                destination_lat, destination_lon = self._extract_coordinates(destination_geocode)

                tool_input = {"tool_input": {"origin": f"{origin_lat},{origin_lon}",
                                             "destination": f"{destination_lat},{destination_lon}"}
                              }
                tool_result = self.route_tool.run(tool_input)
                distance, duration = self._extract_route_info(tool_result)
                result = NavigationResult(
                    action="route",
                    routing_result=RoutingResult(
                        origin=params["origin"],
                        destination=params["destination"],
                        distance_km=distance,
                        duration_hours=duration
                    ),
                    raw_response=raw_output
                )
            elif action == "discover":
                tool_result = self.discover_tool._run(params)
                result = NavigationResult(
                    action="discover",
                    discover_result=DiscoverResult(query=params["q"], results=tool_result),
                    raw_response=raw_output
                )
            elif action == "autosuggest":
                tool_result = self.autosuggest_tool._run(params)
                result = NavigationResult(
                    action="autosuggest",
                    autosuggest_result=AutosuggestResult(query=params["q"], suggestions=tool_result),
                    raw_response=raw_output
                )
            else:
                raise ValueError(f"Unknown action: {action}")

            return result
        except Exception as e:
            return NavigationResult(
                action="error",
                raw_response=f"An error occurred: {str(e)}. Please try rephrasing your query."
            )

    def _parse_raw_output(self, raw_output: str) -> Tuple[str, Dict[str, str]]:
        cleaned_output = re.sub(r'```yaml\n|```\n?', '', raw_output).strip()

        try:
            parsed = yaml.safe_load(cleaned_output)
            if not isinstance(parsed, dict):
                raise ValueError("Parsed output is not a dictionary")

            action = parsed.get('action')
            params = parsed.get('params', {})

            if not action or not params:
                raise ValueError("Missing 'action' or 'params' in parsed output")

            return action, params
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML: {e}")

    def _extract_coordinates(self, geocode_result: str) -> Tuple[float, float]:
        match = re.search(r"Latitude ([-\d.]+), Longitude ([-\d.]+)", geocode_result)
        if match:
            return float(match.group(1)), float(match.group(2))
        raise ValueError("Could not extract coordinates from geocode result")

    def _extract_route_info(self, route_result: str) -> Tuple[float, float]:
        distance_match = re.search(r"Distance ([\d.]+) km", route_result)
        duration_match = re.search(r"Duration ([\d.]+) hours", route_result)
        if distance_match and duration_match:
            return float(distance_match.group(1)), float(duration_match.group(1))
        raise ValueError("Could not extract route info from result")
