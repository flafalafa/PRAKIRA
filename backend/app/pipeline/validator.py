"""Schema validation for incoming raw DTOs."""
from typing import Any
from app.pipeline.exceptions import SchemaValidationFailed
from app.core.logger import get_logger

logger = get_logger(__name__)

class SchemaValidator:
    @staticmethod
    def validate_raw(raw_dto: Any) -> bool:
        if not raw_dto:
            raise SchemaValidationFailed("Raw DTO is empty or None.")
        if not isinstance(raw_dto, (dict, list)) and not hasattr(raw_dto, "model_dump"):
            raise SchemaValidationFailed("Raw DTO must be a dictionary, list, or Pydantic model.")
        return True
