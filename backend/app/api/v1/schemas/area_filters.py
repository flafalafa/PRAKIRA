"""Area API Filters."""
from pydantic import BaseModel, Field
from typing import Optional

class AreaFilterParams(BaseModel):
    status: Optional[str] = None
    active: Optional[bool] = None
    search: Optional[str] = None
    area_type: Optional[str] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
