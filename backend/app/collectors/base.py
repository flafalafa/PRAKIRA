"""Base classes for Collectors."""
from abc import ABC
from typing import Any, Dict
from app.collectors.interfaces import IProvider
from app.config.settings import settings

class BaseCollector(IProvider, ABC):
    """
    Abstract base implementation of IProvider.
    Handles standard configuration reading (retries, timeouts) 
    and common structural needs.
    """
    def __init__(self, config_key: str):
        self.config_key = config_key
        # Typically load from settings, fallback to defaults
        # Assume settings.COLLECTORS is a dict or similar structure in config
        col_settings = getattr(settings, "COLLECTORS", {}).get(config_key, {})
        self.timeout = col_settings.get("timeout", 10)
        self.retry_count = col_settings.get("retry_count", 3)
        self.retry_delay = col_settings.get("retry_delay", 2)
        self.is_enabled = col_settings.get("enabled", True)
        
    async def connect(self) -> None:
        # Default empty implementation, can be overridden
        pass
        
    async def disconnect(self) -> None:
        # Default empty implementation, can be overridden
        pass
        
    async def health(self) -> bool:
        # Default implementation simply checks if enabled
        return self.is_enabled
        
    async def metadata(self) -> Dict[str, Any]:
        return {
            "name": self.__class__.__name__,
            "timeout": self.timeout,
            "retry_count": self.retry_count,
            "enabled": self.is_enabled
        }
