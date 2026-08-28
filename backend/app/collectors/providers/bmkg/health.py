"""BMKG Health Check module."""
import httpx
from enum import Enum
from app.collectors.providers.bmkg.config import BMKGConfig
from app.core.logger import get_logger

logger = get_logger(__name__)

class HealthStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"

class BMKGHealthCheck:
    @staticmethod
    async def check(config: BMKGConfig) -> dict:
        url = f"{config.base_url}{config.endpoint_xml}"
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    return {"status": HealthStatus.AVAILABLE, "latency_ms": response.elapsed.total_seconds() * 1000}
                else:
                    return {"status": HealthStatus.DEGRADED, "reason": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"BMKG Health Check Failed: {str(e)}")
            return {"status": HealthStatus.UNAVAILABLE, "reason": str(e)}
