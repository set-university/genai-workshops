from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from api.here import HereAPI
from typing import Dict, Any
class GeocodeInput(BaseModel):
    address: str = Field(..., description="The address to geocode")

class GeocodeInput(BaseModel):
    address: str = Field(..., description="The address to geocode")

class GeocodeTool(BaseTool):
    name = "geocode"
    description = "Useful for converting an address into geographic coordinates (latitude and longitude)."
    args_schema = GeocodeInput
    api: HereAPI

    def _run(self, tool_input: Dict[str, Any]) -> str:
        print("Tool input is ", tool_input)
        # address = tool_input['address']
        print("Address is ", tool_input)
        address = tool_input
        result = self.api.geocode(address)
        print("Geocode result is ", result)
        if result.get('items'):
            item = result['items'][0]
            return f"Coordinates for '{address}': Latitude {item['position']['lat']}, Longitude {item['position']['lng']}"
        return f"Unable to geocode the address: {address}"

    async def _arun(self, tool_input: Dict[str, Any]) -> str:
        return self._run(tool_input)