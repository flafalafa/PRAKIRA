"""The BMKG Provider implementation."""
from typing import Any, Dict
from app.collectors.base import BaseCollector
from app.collectors.dto.raw import RawPayload
from app.collectors.dto.normalized import NormalizedData
from app.collectors.providers.bmkg.config import get_bmkg_config
from app.collectors.providers.bmkg.client import BMKGClient
from app.collectors.providers.bmkg.parser import BMKGParser
from app.collectors.providers.bmkg.normalizer import BMKGNormalizer
from app.collectors.providers.bmkg.validator import BMKGValidator
from app.collectors.providers.bmkg.health import BMKGHealthCheck, HealthStatus
from app.collectors.registry import CollectorRegistry
from datetime import datetime, timezone
import app.pipeline.transformers.bmkg_transformer  # Auto-registers transformer

class BMKGCollector(BaseCollector):
    def __init__(self, config_key: str = "BMKG"):
        super().__init__(config_key)
        self.config = get_bmkg_config()
        self.client = BMKGClient(self.config)
        
    async def connect(self) -> None:
        await self.client.connect()
        
    async def disconnect(self) -> None:
        await self.client.disconnect()
        
    async def fetch(self, **kwargs) -> RawPayload:
        adm4_code = kwargs.get("adm4_code")
        area_id = kwargs.get("area_id")
        
        if not adm4_code and area_id:
            adm4_code = self.config.area_mappings.get(area_id)
            
        if not adm4_code:
            raise ValueError("BMKGCollector requires 'adm4_code' kwarg or a mapped 'area_id'.")
            
        raw_json = await self.client.fetch_data(adm4_code)
        return RawPayload(
            provider_id="BMKG",
            fetch_time=datetime.now(timezone.utc),
            raw_content=raw_json
        )
        
    async def parse(self, raw_data: RawPayload) -> Any:
        return BMKGParser.parse_data(raw_data.raw_content)
        
    async def normalize(self, parsed_data: Any) -> NormalizedData:
        return BMKGNormalizer.normalize(parsed_data)
        
    async def validate(self, normalized_data: NormalizedData) -> bool:
        return BMKGValidator.validate(normalized_data)
        
    async def health(self) -> bool:
        health_data = await BMKGHealthCheck.check(self.config)
        return health_data.get("status") == HealthStatus.AVAILABLE
        
    async def metadata(self) -> Dict[str, Any]:
        base_meta = await super().metadata()
        health_data = await BMKGHealthCheck.check(self.config)
        base_meta.update({"health": health_data})
        return base_meta

# Register the provider automatically when this module is imported
CollectorRegistry.register("BMKG", BMKGCollector)
