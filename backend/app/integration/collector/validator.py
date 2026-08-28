"""Validates collector implementations and pipeline constraints."""
import inspect
from app.integration.collector.contracts import CollectorContract
from app.integration.collector.exceptions import CollectorContractViolation, CanonicalValidationFailure
from app.pipeline.canonical import CanonicalRecord
from app.core.logger import get_logger

logger = get_logger(__name__)

class SystemValidator:
    @staticmethod
    def validate_collector_contract(collector_instance) -> bool:
        if not isinstance(collector_instance, CollectorContract):
            msg = f"Collector {collector_instance.__class__.__name__} does not implement CollectorContract fully."
            logger.error(msg)
            raise CollectorContractViolation(msg)
        return True
        
    @staticmethod
    def validate_canonical_consistency(record: CanonicalRecord) -> bool:
        if not record.timestamp.tzinfo:
            raise CanonicalValidationFailure("Timestamp must have timezone info.")
        if not record.location.spatial_reference:
            raise CanonicalValidationFailure("Spatial reference missing.")
            
        return True
