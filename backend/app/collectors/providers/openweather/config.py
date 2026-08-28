"""OpenWeather Collector configuration."""
from typing import Optional
from pydantic import BaseModel
from app.core.config import settings

class OpenWeatherConfig(BaseModel):
    enabled: bool = True
    base_url: str = "https://api.openweathermap.org/data/2.5"
    api_key: str = "" # Should be loaded from env/settings
    timeout: int = 15
    retry_count: int = 3
    retry_delay: int = 2
    
def get_openweather_config() -> OpenWeatherConfig:
    ow_settings = getattr(settings, "OPENWEATHER_COLLECTOR", {})
    return OpenWeatherConfig(**ow_settings)
