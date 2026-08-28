"""River Collector configuration."""
from typing import Optional, Dict
from pydantic import BaseModel
from app.core.config import settings

class ProviderConfig(BaseModel):
    name: str
    endpoint: str
    api_key: Optional[str] = None

class RiverConfig(BaseModel):
    enabled: bool = True
    timeout: int = 15
    retry_count: int = 3
    retry_delay: int = 2
    # Support multiple providers (e.g., bbws, bpbd, iot)
    providers: Dict[str, ProviderConfig] = {
        "default_bbws": ProviderConfig(name="BBWS", endpoint="https://api.bbws.go.id/waterlevel")
    }
    
def get_river_config() -> RiverConfig:
    river_settings = getattr(settings, "RIVER_COLLECTOR", {})
    return RiverConfig(**river_settings)
