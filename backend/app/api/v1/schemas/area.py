"""Area API Schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.api.v1.schemas.location import LocationResponse

class AreaResponse(BaseModel):
    area_id: str
    area_name: str
    area_code: str
    status: str
    area_type: str
    location: Optional[LocationResponse] = None
    created_at: datetime
    updated_at: datetime
