"""The Core Collector Pipeline Engine."""
from typing import Any
from app.core.logger import get_logger
from app.collectors.interfaces import IProvider
from app.collectors.context import CollectorContext
from app.collectors.exceptions import (
    ProviderUnavailable, InvalidPayload, NormalizationFailed, ValidationFailed
)

logger = get_logger(__name__)

class CollectorPipeline:
    """
    Orchestrates the strict flow of data collection:
    Fetch -> Parse -> Normalize -> Validate -> Transform -> Persist -> Emit
    """
    def __init__(self, provider: IProvider):
        self.provider = provider
        
    async def execute(self, context: CollectorContext, **kwargs) -> Any:
        provider_name = self.provider.__class__.__name__
        logger.info(f"Collector Started: {provider_name} (Job: {context.job_id})")
        
        try:
            # 1. Connect
            await self.provider.connect()
            
            # 2. Fetch
            logger.debug(f"Fetch Started: {provider_name}")
            raw_data = await self.provider.fetch(**kwargs)
            logger.debug(f"Fetch Completed: {provider_name}")
            
            # 3. Parse
            parsed_data = await self.provider.parse(raw_data)
            
            # 4. Normalize
            logger.debug(f"Normalization Started: {provider_name}")
            normalized_data = await self.provider.normalize(parsed_data)
            
            # 5. Validate
            is_valid = await self.provider.validate(normalized_data)
            if not is_valid:
                logger.error(f"Validation Failed: {provider_name}")
                raise ValidationFailed(f"Data from {provider_name} failed structural validation.")
                
            # 6 & 7. Transform to Domain Entity, Persist, Emit (Future)
            # Will be implemented when Application Services bridge Collectors to Domain
            
            context.mark_completed()
            logger.info(f"Collector Finished: {provider_name} in {context.get_duration_ms():.2f}ms")
            
            return normalized_data
            
        except Exception as e:
            context.add_error(e)
            logger.error(f"Collector Error in {provider_name}: {str(e)}")
            raise
        finally:
            await self.provider.disconnect()
