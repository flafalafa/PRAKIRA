"""RainViewer Health Check module."""
import httpx
from enum import Enum
from app.collectors.providers.rainviewer.config import RainViewerConfig
from app.core.logger import get_logger

logger = get_logger(__name__)

class HealthStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"

class RainViewerHealthCheck:
    @staticmethod
    async def check(config: RainViewerConfig) -> dict:
        url = config.base_url
        
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    has_frames = bool(data.get("radar", {}).get("past"))
                    if has_frames:
                        return {"status": HealthStatus.AVAILABLE, "latency_ms": response.elapsed.total_seconds() * 1000}
                    else:
                        return {"status": HealthStatus.DEGRADED, "reason": "No radar frames available in response"}
                else:
                    return {"status": HealthStatus.DEGRADED, "reason": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"RainViewer Health Check Failed: {str(e)}")
            return {"status": HealthStatus.UNAVAILABLE, "reason": str(e)}
