"""Normalizes transformed data into Canonical Models."""
from typing import Dict, Any, List
from app.pipeline.canonical import CanonicalRecord
from app.pipeline.exceptions import NormalizationFailed
from app.pipeline.context import PipelineContext
from app.core.logger import get_logger

logger = get_logger(__name__)

class DataNormalizer:
    @staticmethod
    def normalize(transformed_data: List[Dict[str, Any]], context: PipelineContext) -> List[CanonicalRecord]:
        records = []
        for idx, item in enumerate(transformed_data):
            try:
                record = CanonicalRecord(**item)
                records.append(record)
            except Exception as e:
                context.add_error("Normalizer", f"Item {idx} failed normalization: {str(e)}")
                raise NormalizationFailed(f"Normalization failed for {context.provider_id}: {str(e)}")
        return records
