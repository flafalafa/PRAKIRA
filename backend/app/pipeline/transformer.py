"""Transforms raw provider data fields to standard names."""
from typing import Any, Dict
from app.pipeline.registry import PipelineRegistry
from app.pipeline.exceptions import TransformationFailed
from app.pipeline.context import PipelineContext
from app.core.logger import get_logger

logger = get_logger(__name__)

class DataTransformer:
    @staticmethod
    def transform(raw_dto: Any, context: PipelineContext) -> Any:
        transformer_func = PipelineRegistry.get_transformer(context.provider_id)
        if not transformer_func:
            logger.warning(f"No specific transformer registered for {context.provider_id}. Using generic.")
            return raw_dto if isinstance(raw_dto, dict) else getattr(raw_dto, "model_dump", lambda: vars(raw_dto))()
            
        try:
            return transformer_func(raw_dto)
        except Exception as e:
            context.add_error("Transformer", str(e))
            raise TransformationFailed(f"Failed to transform data for {context.provider_id}: {str(e)}")
