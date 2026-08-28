"""Asynchronous HTTP Client for River Telemetry."""
import httpx
import asyncio
from typing import Dict, Any
from app.core.logger import get_logger
from app.collectors.providers.river.config import RiverConfig, ProviderConfig
from app.collectors.providers.river.exceptions import (
    RiverConnectionError, RiverTimeoutError
)

logger = get_logger(__name__)

class RiverClient:
    def __init__(self, config: RiverConfig):
        self.config = config
        self._client: httpx.AsyncClient | None = None
        
    async def connect(self):
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.config.timeout)
            logger.debug("River HTTP client connected.")
            
    async def disconnect(self):
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.debug("River HTTP client disconnected.")
            
    async def fetch_telemetry(self, provider: ProviderConfig) -> Any:
        if not self._client:
            await self.connect()
            
        url = provider.endpoint
        headers = {}
        if provider.api_key:
            headers["Authorization"] = f"Bearer {provider.api_key}"
            
        for attempt in range(self.config.retry_count):
            try:
                logger.debug(f"River request sent to {provider.name} (Attempt {attempt+1})")
                response = await self._client.get(url, headers=headers)
                
                response.raise_for_status()
                logger.debug(f"River response received from {provider.name}.")
                return response.json()
                
            except httpx.TimeoutException as e:
                logger.warning(f"River timeout on attempt {attempt+1}: {str(e)}")
                if attempt == self.config.retry_count - 1:
                    raise RiverTimeoutError(f"Request timed out after {self.config.retry_count} attempts.")
            except httpx.RequestError as e:
                logger.warning(f"River connection error on attempt {attempt+1}: {str(e)}")
                if attempt == self.config.retry_count - 1:
                    raise RiverConnectionError(f"Request failed: {str(e)}")
                    
            await asyncio.sleep(self.config.retry_delay * (2 ** attempt))
            
        raise RiverConnectionError("River request failed unexpectedly.")
