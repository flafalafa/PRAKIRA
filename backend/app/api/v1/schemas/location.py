"""Location API Schemas."""
from pydantic import BaseModel
from typing import Optional

class LocationResponse(BaseModel):
    latitude: float
    longitude: float
    precision: Optional[str] = None
    timezone: str = "Asia/Jakarta"
    country: str = "Indonesia"
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    subdistrict: Optional[str] = None
