from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from api.here import HereAPI


class DiscoverInput(BaseModel):
    q: str = Field(..., description="The search query for discovering places or addresses")
    at: Optional[str] = Field(None, description="Optional latitude,longitude for location-based search")


class DiscoverTool(BaseTool):
    name = "discover"
    description = "Useful for searching places or addresses based on free-form queries."
    args_schema = DiscoverInput
    api: HereAPI

    def _run(self, tool_input: Dict[str, Any]) -> str:
        query = tool_input['q']
        at = tool_input.get('at')

        params = {
            "q": query,
            "limit": 5
        }
        if at:
            params["at"] = at

        result = self.api.discover(params)

        if result.get('items'):
            output = f"Discovered places for '{query}':\n"
            for item in result['items']:
                output += f"- {item['title']}: Latitude {item['position']['lat']}, Longitude {item['position']['lng']}\n"
            return output
        return f"Unable to find places matching: {query}"

    async def _arun(self, tool_input: Dict[str, Any]) -> str:
        return self._run(tool_input)