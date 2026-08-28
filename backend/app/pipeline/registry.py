"""Pipeline Provider Rules Registry."""
from typing import Dict, Any, Callable
from app.core.logger import get_logger

logger = get_logger(__name__)

class PipelineRegistry:
    _transformers: Dict[str, Callable] = {}
    
    @classmethod
    def register_transformer(cls, provider_id: str, func: Callable) -> None:
        cls._transformers[provider_id] = func
        logger.debug(f"Registered transformer for provider: {provider_id}")
        
    @classmethod
    def get_transformer(cls, provider_id: str) -> Callable:
        return cls._transformers.get(provider_id)
