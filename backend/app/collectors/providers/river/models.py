"""River specific data models."""
from typing import Any, Dict, List
from pydantic import BaseModel

class RiverRawData(BaseModel):
    """Raw data from a river telemetry provider."""
    raw_payload: Any
    provider_name: str
    endpoint: str
    
class StationData(BaseModel):
    station_id: str
    name: str
    lat: float
    lon: float
    water_level: float
    flow_rate: float
    status: str
    timestamp: str

class RiverParsedData(BaseModel):
    """Parsed dictionary representation of River payload."""
    provider_name: str
    stations: List[StationData]
