from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from api.here import HereAPI
from typing import Dict, Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from api.here import HereAPI

class RouteInput(BaseModel):
    route_query: str = Field(..., description="The origin and destination of the route, separated by ' to '. For example: 'New York to Los Angeles'")

class RouteTool(BaseTool):
    name = "route"
    description = "Useful for calculating a route between two locations and getting the distance and travel time. Input should be in the format 'origin to destination'."
    args_schema = RouteInput
    api: HereAPI

    def _run(self, tool_input: Dict[str, Any]) -> str:
        print("Tool input is ", tool_input)
        """Params is  {'origin': 'Berlin, Germany', 'destination': 'Munich, Germany'}
"""
        origin, destination = tool_input['origin'], tool_input['destination']
        print("Origin is ", origin)
        print("Destination is ", destination)
        result = self.api.calculate_route(origin, destination)
        print("Result is ", result)
        if result.get('routes'):
            route = result['routes'][0]
            summary = route['sections'][0]['summary']
            return f"Route from {origin} to {destination}: Distance {summary['length']/1000:.2f} km, Duration {summary['duration']/3600:.2f} hours"
        return f"Unable to calculate route from {origin} to {destination}"

    async def _arun(self, tool_input: Dict[str, Any]) -> str:
        return self._run(tool_input)