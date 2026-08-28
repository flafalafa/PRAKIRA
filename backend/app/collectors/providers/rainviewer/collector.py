"""The RainViewer Provider implementation."""
from typing import Any, Dict
from app.collectors.base import BaseCollector
from app.collectors.dto.raw import RawPayload
from app.collectors.dto.normalized import NormalizedData
from app.collectors.providers.rainviewer.config import get_rainviewer_config
from app.collectors.providers.rainviewer.client import RainViewerClient
from app.collectors.providers.rainviewer.parser import RainViewerParser
from app.collectors.providers.rainviewer.normalizer import RainViewerNormalizer
from app.collectors.providers.rainviewer.validator import RainViewerValidator
from app.collectors.providers.rainviewer.health import RainViewerHealthCheck, HealthStatus
from app.collectors.registry import CollectorRegistry
from datetime import datetime, timezone

class RainViewerCollector(BaseCollector):
    def __init__(self, config_key: str = "RAINVIEWER"):
        super().__init__(config_key)
        self.config = get_rainviewer_config()
        self.client = RainViewerClient(self.config)
        
    async def connect(self) -> None:
        await self.client.connect()
        
    async def disconnect(self) -> None:
        await self.client.disconnect()
        
    async def fetch(self, **kwargs) -> RawPayload:
        raw_json = await self.client.fetch_weather_maps()
        return RawPayload(
            provider_id="RainViewer",
            fetch_time=datetime.now(timezone.utc),
            raw_content=raw_json
        )
        
    async def parse(self, raw_data: RawPayload) -> Any:
        return RainViewerParser.parse_maps(raw_data.raw_content)
        
    async def normalize(self, parsed_data: Any) -> NormalizedData:
        return RainViewerNormalizer.normalize(parsed_data)
        
    async def validate(self, normalized_data: NormalizedData) -> bool:
        return RainViewerValidator.validate(normalized_data)
        
    async def health(self) -> bool:
        health_data = await RainViewerHealthCheck.check(self.config)
        return health_data.get("status") == HealthStatus.AVAILABLE
        
    async def metadata(self) -> Dict[str, Any]:
        base_meta = await super().metadata()
        health_data = await RainViewerHealthCheck.check(self.config)
        base_meta.update({"health": health_data})
        return base_meta

# Register the provider
CollectorRegistry.register("RainViewer", RainViewerCollector)
