"""OpenWeather specific data models."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class OpenWeatherRawData(BaseModel):
    """Raw JSON data from OpenWeather API."""
    raw_json: Dict[str, Any]
    endpoint: str
    
class OpenWeatherParsedData(BaseModel):
    """Parsed dictionary representation of OpenWeather payload."""
    lat: float
    lon: float
    timezone: str
    current: Optional[Dict[str, Any]] = None
    hourly: Optional[List[Dict[str, Any]]] = None
    daily: Optional[List[Dict[str, Any]]] = None
    alerts: Optional[List[Dict[str, Any]]] = None
