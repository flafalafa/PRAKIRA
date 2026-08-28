"""RainViewer specific data models."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class RainViewerRawData(BaseModel):
    """Raw JSON data from RainViewer API."""
    raw_json: Dict[str, Any]
    endpoint: str
    
class RainViewerParsedData(BaseModel):
    """Parsed dictionary representation of RainViewer payload."""
    version: str
    generated: int
    host: str
    radar: Dict[str, Any]
    satellite: Dict[str, Any]
