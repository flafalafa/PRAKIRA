"""Common API Schemas."""
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

class Meta(BaseModel):
    request_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = "v1"
