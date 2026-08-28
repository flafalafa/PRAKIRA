"""Error Response Schemas."""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime, timezone

class ApiError(BaseModel):
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    request_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    path: str = ""
    version: str = "v1"
