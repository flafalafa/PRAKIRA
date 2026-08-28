"""The OpenWeather Provider implementation."""
from typing import Any, Dict
from app.collectors.base import BaseCollector
from app.collectors.dto.raw import RawPayload
from app.collectors.dto.normalized import NormalizedData
from app.collectors.providers.openweather.config import get_openweather_config
from app.collectors.providers.openweather.client import OpenWeatherClient
from app.collectors.providers.openweather.parser import OpenWeatherParser
from app.collectors.providers.openweather.normalizer import OpenWeatherNormalizer
from app.collectors.providers.openweather.validator import OpenWeatherValidator
from app.collectors.providers.openweather.health import OpenWeatherHealthCheck, HealthStatus
from app.collectors.registry import CollectorRegistry
from datetime import datetime, timezone

class OpenWeatherCollector(BaseCollector):
    def __init__(self, config_key: str = "OPENWEATHER"):
        super().__init__(config_key)
        self.config = get_openweather_config()
        self.client = OpenWeatherClient(self.config)
        
    async def connect(self) -> None:
        await self.client.connect()
        
    async def disconnect(self) -> None:
        await self.client.disconnect()
        
    async def fetch(self, lat: float = -6.2, lon: float = 106.8, **kwargs) -> RawPayload:
        raw_json = await self.client.fetch_onecall(lat=lat, lon=lon)
        return RawPayload(
            provider_id="OpenWeather",
            fetch_time=datetime.now(timezone.utc),
            raw_content=raw_json
        )
        
    async def parse(self, raw_data: RawPayload) -> Any:
        return OpenWeatherParser.parse_onecall(raw_data.raw_content)
        
    async def normalize(self, parsed_data: Any) -> NormalizedData:
        return OpenWeatherNormalizer.normalize(parsed_data)
        
    async def validate(self, normalized_data: NormalizedData) -> bool:
        return OpenWeatherValidator.validate(normalized_data)
        
    async def health(self) -> bool:
        health_data = await OpenWeatherHealthCheck.check(self.config)
        return health_data.get("status") == HealthStatus.AVAILABLE
        
    async def metadata(self) -> Dict[str, Any]:
        base_meta = await super().metadata()
        health_data = await OpenWeatherHealthCheck.check(self.config)
        base_meta.update({"health": health_data})
        return base_meta

# Register the provider
CollectorRegistry.register("OpenWeather", OpenWeatherCollector)
