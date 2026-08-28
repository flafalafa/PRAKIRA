"""Validates the health endpoints of all integrated components."""
from app.integration.collector.registry import IntegrationRegistry
from app.core.logger import get_logger

logger = get_logger(__name__)

class IntegrationHealth:
    @staticmethod
    async def check_all() -> dict:
        results = {}
        collectors = IntegrationRegistry.get_registered_collectors()
        for name, collector_class in collectors.items():
            try:
                instance = collector_class()
                is_healthy = await instance.health()
                results[name] = "AVAILABLE" if is_healthy else "DEGRADED"
            except Exception as e:
                logger.error(f"Health check failed for {name}: {str(e)}")
                results[name] = "UNAVAILABLE"
        return results
