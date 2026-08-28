"""Normalized DTOs for mapping external data into canonical structures."""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

class NormalizedData(BaseModel):
    """
    Canonical structure that represents data after it has been scrubbed,
    typed, and mapped to Flood Guardian's internal conventions.
    Will later be transformed into Domain Entities.
    """
    provider_id: str
    normalized_time: datetime
    
    # Generic buckets for data mapping
    location_data: Optional[Dict[str, Any]] = None
    weather_data: Optional[Dict[str, Any]] = None
    hydrology_data: Optional[Dict[str, Any]] = None
    
    # Can contain multiple readings (e.g. hourly forecast array)
    time_series: Optional[List[Dict[str, Any]]] = None
