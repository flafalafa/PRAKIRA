"""Enterprise Data Normalization Pipeline orchestrator."""
import uuid
from typing import Any, List
from app.pipeline.context import PipelineContext
from app.pipeline.validator import SchemaValidator
from app.pipeline.transformer import DataTransformer
from app.pipeline.normalizer import DataNormalizer
from app.pipeline.quality import QualityValidator
from app.pipeline.enricher import DataEnricher
from app.pipeline.canonical import CanonicalRecord
from app.core.logger import get_logger

logger = get_logger(__name__)

class EnterprisePipeline:
    @staticmethod
    def process(raw_dto: Any, provider_id: str) -> List[CanonicalRecord]:
        trace_id = str(uuid.uuid4())
        context = PipelineContext(trace_id=trace_id, provider_id=provider_id)
        logger.info(f"Pipeline started for trace: {trace_id} (Provider: {provider_id})")
        
        try:
            # 1. Schema Validation
            logger.debug("Running Schema Validation.")
            SchemaValidator.validate_raw(raw_dto)
            
            # 2. Transformation
            logger.debug("Running Transformation.")
            transformed = DataTransformer.transform(raw_dto, context)
            
            # Ensure transformed data is a list for the normalizer
            if not isinstance(transformed, list):
                transformed = [transformed]
                
            # 3. Normalization -> Canonical DTO
            logger.debug("Running Normalization.")
            canonical_records = DataNormalizer.normalize(transformed, context)
            
            # 4. Quality Validation
            logger.debug("Running Quality Validation.")
            validated_records = QualityValidator.validate(canonical_records, context)
            
            # 5. Enrichment
            logger.debug("Running Enrichment.")
            enriched_records = DataEnricher.enrich(validated_records, context)
            
            logger.info(f"Pipeline finished for trace: {trace_id}. Produced {len(enriched_records)} records.")
            return enriched_records
            
        except Exception as e:
            logger.error(f"Pipeline failed for trace: {trace_id}: {str(e)}")
            for err in context.errors:
                logger.error(f"  - {err}")
            raise
