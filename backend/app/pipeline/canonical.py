"""Flood Guardian Canonical Data Model."""
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field

class LocationMetadata(BaseModel):
    latitude: float
    longitude: float
    elevation: Optional[float] = None
    spatial_reference: str = "WGS84"

class ObservationMetadata(BaseModel):
    provider_id: str
    station_id: Optional[str] = None
    sensor_type: Optional[str] = None

class CanonicalMeasurement(BaseModel):
    parameter: str
    value: float
    unit: str
    quality_score: Optional[float] = 1.0

class CanonicalRecord(BaseModel):
    record_id: str
    timestamp: datetime
    location: LocationMetadata
    metadata: ObservationMetadata
    measurements: List[CanonicalMeasurement]
    enrichment_tags: Dict[str, str] = Field(default_factory=dict)
