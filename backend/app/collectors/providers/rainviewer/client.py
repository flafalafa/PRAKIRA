"""Asynchronous HTTP Client for RainViewer."""
import httpx
import asyncio
from app.core.logger import get_logger
from app.collectors.providers.rainviewer.config import RainViewerConfig
from app.collectors.providers.rainviewer.exceptions import (
    RainViewerConnectionError, RainViewerTimeoutError
)

logger = get_logger(__name__)

class RainViewerClient:
    def __init__(self, config: RainViewerConfig):
        self.config = config
        self._client: httpx.AsyncClient | None = None
        
    async def connect(self):
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.config.timeout)
            logger.debug("RainViewer HTTP client connected.")
            
    async def disconnect(self):
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.debug("RainViewer HTTP client disconnected.")
            
    async def fetch_weather_maps(self) -> dict:
        if not self._client:
            await self.connect()
            
        url = self.config.base_url
        
        for attempt in range(self.config.retry_count):
            try:
                logger.debug(f"RainViewer request sent (Attempt {attempt+1})")
                response = await self._client.get(url)
                
                response.raise_for_status()
                logger.debug("RainViewer response received successfully.")
                return response.json()
                
            except httpx.TimeoutException as e:
                logger.warning(f"RainViewer timeout on attempt {attempt+1}: {str(e)}")
                if attempt == self.config.retry_count - 1:
                    raise RainViewerTimeoutError(f"Request timed out after {self.config.retry_count} attempts.")
            except httpx.RequestError as e:
                logger.warning(f"RainViewer connection error on attempt {attempt+1}: {str(e)}")
                if attempt == self.config.retry_count - 1:
                    raise RainViewerConnectionError(f"Request failed: {str(e)}")
                    
            # Exponential backoff
            await asyncio.sleep(self.config.retry_delay * (2 ** attempt))
            
        raise RainViewerConnectionError("RainViewer request failed unexpectedly.")
