"""OpenWeather Health Check module."""
import httpx
from enum import Enum
from app.collectors.providers.openweather.config import OpenWeatherConfig
from app.core.logger import get_logger

logger = get_logger(__name__)

class HealthStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"

class OpenWeatherHealthCheck:
    @staticmethod
    async def check(config: OpenWeatherConfig) -> dict:
        if not config.api_key:
            return {"status": HealthStatus.UNAVAILABLE, "reason": "Missing API Key"}
            
        # Using simple weather endpoint for health check to save heavy onecall quota
        url = f"{config.base_url}/weather"
        params = {"q": "Jakarta", "appid": config.api_key}
        
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    return {"status": HealthStatus.AVAILABLE, "latency_ms": response.elapsed.total_seconds() * 1000}
                elif response.status_code in (401, 403):
                    return {"status": HealthStatus.UNAVAILABLE, "reason": "Authentication Failed"}
                elif response.status_code == 429:
                    return {"status": HealthStatus.DEGRADED, "reason": "Rate Limited"}
                else:
                    return {"status": HealthStatus.DEGRADED, "reason": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"OpenWeather Health Check Failed: {str(e)}")
            return {"status": HealthStatus.UNAVAILABLE, "reason": str(e)}
