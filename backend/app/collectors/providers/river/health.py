"""River Health Check module."""
import httpx
from enum import Enum
from app.collectors.providers.river.config import RiverConfig
from app.core.logger import get_logger

logger = get_logger(__name__)

class HealthStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"

class RiverHealthCheck:
    @staticmethod
    async def check(config: RiverConfig) -> dict:
        results = {}
        async with httpx.AsyncClient(timeout=5) as client:
            for provider_key, provider in config.providers.items():
                try:
                    url = provider.endpoint
                    headers = {"Authorization": f"Bearer {provider.api_key}"} if provider.api_key else {}
                    
                    response = await client.get(url, headers=headers)
                    if response.status_code == 200:
                        results[provider_key] = {"status": HealthStatus.AVAILABLE, "latency_ms": response.elapsed.total_seconds() * 1000}
                    else:
                        results[provider_key] = {"status": HealthStatus.DEGRADED, "reason": f"HTTP {response.status_code}"}
                except Exception as e:
                    logger.error(f"River Health Check Failed for {provider.name}: {str(e)}")
                    results[provider_key] = {"status": HealthStatus.UNAVAILABLE, "reason": str(e)}
                    
        return results
