"""Tracks all components ready for integration."""
from typing import Dict, Any, List
from app.collectors.registry import CollectorRegistry
from app.core.logger import get_logger

logger = get_logger(__name__)

class IntegrationRegistry:
    @staticmethod
    def get_registered_collectors() -> Dict[str, Any]:
        return CollectorRegistry._registry
        
    @staticmethod
    def get_registered_providers() -> List[str]:
        return list(CollectorRegistry._registry.keys())
