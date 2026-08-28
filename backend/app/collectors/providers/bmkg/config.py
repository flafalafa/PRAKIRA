"""BMKG Collector configuration."""
from typing import Dict, Optional, Any
from pydantic import BaseModel
from app.config.settings import settings

class BMKGConfig(BaseModel):
    enabled: bool = True
    base_url: str = "https://api.bmkg.go.id/publik/prakiraan-cuaca"
    timeout: int = 15
    retry_count: int = 3
    retry_delay: int = 2
    area_mappings: dict = {"area-1": "31.71.06.1001"}
    
def get_bmkg_config() -> BMKGConfig:
    # Safely load from settings if exists, else return default
    bmkg_settings = getattr(settings, "BMKG_COLLECTOR", {})
    return BMKGConfig(**bmkg_settings)
