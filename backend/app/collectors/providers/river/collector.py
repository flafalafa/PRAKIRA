"""The River Provider implementation."""
from typing import Any, Dict
from app.collectors.base import BaseCollector
from app.collectors.dto.raw import RawPayload
from app.collectors.dto.normalized import NormalizedData
from app.collectors.providers.river.config import get_river_config
from app.collectors.providers.river.client import RiverClient
from app.collectors.providers.river.parser import RiverParser
from app.collectors.providers.river.normalizer import RiverNormalizer
from app.collectors.providers.river.validator import RiverValidator
from app.collectors.providers.river.health import RiverHealthCheck
from app.collectors.registry import CollectorRegistry
from datetime import datetime, timezone

class RiverCollector(BaseCollector):
    def __init__(self, config_key: str = "RIVER"):
        super().__init__(config_key)
        self.config = get_river_config()
        self.client = RiverClient(self.config)
        
    async def connect(self) -> None:
        await self.client.connect()
        
    async def disconnect(self) -> None:
        await self.client.disconnect()
        
    async def fetch(self, provider_key: str = "default_bbws", **kwargs) -> RawPayload:
        provider = self.config.providers.get(provider_key)
        if not provider:
            raise ValueError(f"Provider key {provider_key} not configured in RiverCollector.")
            
        raw_json = await self.client.fetch_telemetry(provider)
        return RawPayload(
            provider_id=provider.name,
            fetch_time=datetime.now(timezone.utc),
            raw_content=raw_json
        )
        
    async def parse(self, raw_data: RawPayload) -> Any:
        return RiverParser.parse_payload(raw_data.raw_content, raw_data.provider_id)
        
    async def normalize(self, parsed_data: Any) -> NormalizedData:
        return RiverNormalizer.normalize(parsed_data)
        
    async def validate(self, normalized_data: NormalizedData) -> bool:
        return RiverValidator.validate(normalized_data)
        
    async def health(self) -> bool:
        health_data = await RiverHealthCheck.check(self.config)
        # Check if at least one provider is AVAILABLE
        return any(info.get("status") == "AVAILABLE" for info in health_data.values())
        
    async def metadata(self) -> Dict[str, Any]:
        base_meta = await super().metadata()
        health_data = await RiverHealthCheck.check(self.config)
        base_meta.update({"health": health_data, "providers": list(self.config.providers.keys())})
        return base_meta

# Register the provider
CollectorRegistry.register("River", RiverCollector)
