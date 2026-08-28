"""Asynchronous HTTP Client for OpenWeather."""
import httpx
import asyncio
from app.core.logger import get_logger
from app.collectors.providers.openweather.config import OpenWeatherConfig
from app.collectors.providers.openweather.exceptions import (
    OpenWeatherConnectionError, OpenWeatherTimeoutError,
    OpenWeatherAuthError, OpenWeatherRateLimitError
)

logger = get_logger(__name__)

class OpenWeatherClient:
    def __init__(self, config: OpenWeatherConfig):
        self.config = config
        self._client: httpx.AsyncClient | None = None
        
    async def connect(self):
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.config.timeout)
            logger.debug("OpenWeather HTTP client connected.")
            
    async def disconnect(self):
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.debug("OpenWeather HTTP client disconnected.")
            
    async def fetch_onecall(self, lat: float, lon: float) -> dict:
        if not self._client:
            await self.connect()
            
        url = f"{self.config.base_url}/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.config.api_key,
            "units": "metric"
        }
        
        for attempt in range(self.config.retry_count):
            try:
                logger.debug(f"OpenWeather request sent (Attempt {attempt+1})")
                response = await self._client.get(url, params=params)
                
                if response.status_code in (401, 403):
                    logger.error("OpenWeather Authentication Failed.")
                    raise OpenWeatherAuthError("Invalid API Key or unauthorized.")
                if response.status_code == 429:
                    logger.error("OpenWeather Rate Limited.")
                    raise OpenWeatherRateLimitError("Rate limit exceeded.")
                    
                response.raise_for_status()
                logger.debug("OpenWeather response received successfully.")
                return response.json()
                
            except httpx.TimeoutException as e:
                logger.warning(f"OpenWeather timeout on attempt {attempt+1}: {str(e)}")
                if attempt == self.config.retry_count - 1:
                    raise OpenWeatherTimeoutError(f"Request timed out after {self.config.retry_count} attempts.")
            except httpx.RequestError as e:
                logger.warning(f"OpenWeather connection error on attempt {attempt+1}: {str(e)}")
                if attempt == self.config.retry_count - 1:
                    raise OpenWeatherConnectionError(f"Request failed: {str(e)}")
                    
            # Exponential backoff
            await asyncio.sleep(self.config.retry_delay * (2 ** attempt))
            
        raise OpenWeatherConnectionError("OpenWeather request failed unexpectedly.")
