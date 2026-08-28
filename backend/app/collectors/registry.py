"""Central registry for all collector providers."""
from typing import Dict, Type
from app.collectors.base import BaseCollector

class CollectorRegistry:
    _providers: Dict[str, Type[BaseCollector]] = {}
    
    @classmethod
    def register(cls, name: str, provider_class: Type[BaseCollector]):
        cls._providers[name] = provider_class
        
    @classmethod
    def get_provider_class(cls, name: str) -> Type[BaseCollector]:
        if name not in cls._providers:
            raise ValueError(f"Provider {name} is not registered.")
        return cls._providers[name]
        
    @classmethod
    def list_providers(cls) -> Dict[str, Type[BaseCollector]]:
        return cls._providers.copy()
