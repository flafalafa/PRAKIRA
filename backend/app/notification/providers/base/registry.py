"""Provider Registry."""
from typing import Dict, List, Optional, Any
from app.notification.providers.base.provider import BasePushProvider
from app.core.logger import get_logger

logger = get_logger(__name__)

class ProviderRegistry:
    _providers: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def register(cls, provider: BasePushProvider, enabled: bool = True) -> None:
        cls._providers[provider.name] = {
            "instance": provider,
            "enabled": enabled,
            "metadata": {}
        }
        logger.debug(f"Registered Push Provider: {provider.name}")
        
    @classmethod
    def get_provider(cls, name: str) -> Optional[BasePushProvider]:
        p = cls._providers.get(name)
        if p and p["enabled"]:
            return p["instance"]
        return None
        
    @classmethod
    def get_all_enabled(cls) -> List[BasePushProvider]:
        return [p["instance"] for p in cls._providers.values() if p["enabled"]]
