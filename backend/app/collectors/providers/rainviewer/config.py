"""RainViewer Collector configuration."""
from typing import Optional
from pydantic import BaseModel
from app.core.config import settings

class RainViewerConfig(BaseModel):
    enabled: bool = True
    base_url: str = "https://api.rainviewer.com/public/weather-maps.json"
    timeout: int = 15
    retry_count: int = 3
    retry_delay: int = 2
    
def get_rainviewer_config() -> RainViewerConfig:
    rv_settings = getattr(settings, "RAINVIEWER_COLLECTOR", {})
    return RainViewerConfig(**rv_settings)
