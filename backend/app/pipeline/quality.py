"""Quality assurance for Canonical Records."""
from typing import List
from app.pipeline.canonical import CanonicalRecord
from app.pipeline.exceptions import QualityValidationFailed
from app.pipeline.context import PipelineContext
from app.core.logger import get_logger

logger = get_logger(__name__)

class QualityValidator:
    @staticmethod
    def validate(records: List[CanonicalRecord], context: PipelineContext) -> List[CanonicalRecord]:
        valid_records = []
        seen_keys = set()
        
        for record in records:
            if not record.measurements:
                context.add_error("Quality", f"Record {record.record_id} has no measurements.")
                continue
                
            if not record.timestamp:
                context.add_error("Quality", f"Record {record.record_id} has no timestamp.")
                continue
                
            unique_key = f"{record.metadata.provider_id}_{record.metadata.station_id}_{record.timestamp.isoformat()}"
            if unique_key in seen_keys:
                context.add_error("Quality", f"Duplicate observation detected: {unique_key}")
                continue
            seen_keys.add(unique_key)
            
            valid_measurements = []
            for m in record.measurements:
                if m.value < -9999 or m.value > 99999:
                    context.add_error("Quality", f"Measurement out of bounds for {m.parameter}: {m.value}")
                else:
                    valid_measurements.append(m)
                    
            if valid_measurements:
                record.measurements = valid_measurements
                valid_records.append(record)
                
        if not valid_records:
            raise QualityValidationFailed("All records failed quality validation.")
            
        return valid_records
