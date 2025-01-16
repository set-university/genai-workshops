from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from api.here import HereAPI


class AutosuggestInput(BaseModel):
    q: str = Field(..., description="The partial input to suggest places or addresses")
    at: Optional[str] = Field(None, description="Optional latitude,longitude for location-based suggestions")


class AutosuggestTool(BaseTool):
    name = "autosuggest"
    description = "Useful for suggesting places or addresses based on incomplete input."
    args_schema = AutosuggestInput
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

        result = self.api.autosuggest(params)

        if result.get('items'):
            output = f"Suggestions for '{query}':\n"
            for item in result['items']:
                output += f"- {item['title']}\n"
            return output
        return f"Unable to generate suggestions for: {query}"

    async def _arun(self, tool_input: Dict[str, Any]) -> str:
        return self._run(tool_input)