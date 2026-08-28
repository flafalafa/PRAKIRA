"""BMKG specific data models/structures."""
from typing import Any, Dict
from pydantic import BaseModel

class BMKGRawData(BaseModel):
    """Raw data structure from BMKG API."""
    raw_xml: str
    region: str
    
class BMKGParsedData(BaseModel):
    """Parsed dictionary representation of BMKG JSON."""
    lokasi: Dict[str, Any]
    data: list[Dict[str, Any]]
