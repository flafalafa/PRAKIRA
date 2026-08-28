"""Asynchronous HTTP Client for BMKG."""
import httpx
import asyncio
from app.core.logger import get_logger
from app.collectors.providers.bmkg.config import BMKGConfig
from app.collectors.providers.bmkg.exceptions import BMKGConnectionError, BMKGTimeoutError

logger = get_logger(__name__)

class BMKGClient:
    def __init__(self, config: BMKGConfig):
        self.config = config
        self._client: httpx.AsyncClient | None = None
        
    async def connect(self):
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.config.timeout)
            logger.debug("BMKG HTTP client connected.")
            
    async def disconnect(self):
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.debug("BMKG HTTP client disconnected.")
            
    async def fetch_data(self, adm4_code: str) -> str:
        if not self._client:
            await self.connect()
            
        url = self.config.base_url
        params = {"adm4": adm4_code}
        
        for attempt in range(self.config.retry_count):
            try:
                logger.debug(f"BMKG request sent: {url} with params {params} (Attempt {attempt+1})")
                response = await self._client.get(url, params=params)
                response.raise_for_status()
                logger.debug("BMKG response received successfully.")
                return response.text
                
            except httpx.TimeoutException as e:
                logger.warning(f"BMKG timeout on attempt {attempt+1}: {str(e)}")
                if attempt == self.config.retry_count - 1:
                    raise BMKGTimeoutError(f"BMKG request timed out after {self.config.retry_count} attempts.")
            except httpx.RequestError as e:
                logger.warning(f"BMKG connection error on attempt {attempt+1}: {str(e)}")
                if attempt == self.config.retry_count - 1:
                    raise BMKGConnectionError(f"BMKG request failed: {str(e)}")
                    
            await asyncio.sleep(self.config.retry_delay)
            
        raise BMKGConnectionError("BMKG request failed unexpectedly.")
