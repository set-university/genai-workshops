from pydantic import BaseModel, Field
from typing import Optional

class GeocodingResult(BaseModel):
    address: str
    latitude: float
    longitude: float

class RoutingResult(BaseModel):
    origin: str
    destination: str
    distance_km: float
    duration_hours: float

class NavigationResult(BaseModel):
    action: str = Field(..., description="The action performed: 'geocode' or 'route'")
    geocoding_result: Optional[GeocodingResult] = None
    routing_result: Optional[RoutingResult] = None
    raw_response: str = Field(..., description="The raw response from the model")