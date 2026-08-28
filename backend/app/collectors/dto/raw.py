"""Raw DTOs for generic collector ingestion."""
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RawPayload(BaseModel):
    """
    Generic wrapper for raw data fetched from a provider.
    No business logic, purely a container for untyped or semi-typed data.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    provider_id: str
    fetch_time: datetime
    raw_content: Any
    metadata: Optional[Dict[str, Any]] = None
