"""Validates the Canonical NormalizedData DTO for River Telemetry."""
from app.collectors.dto.normalized import NormalizedData
from app.core.logger import get_logger

logger = get_logger(__name__)

class RiverValidator:
    @staticmethod
    def validate(normalized_data: NormalizedData) -> bool:
        if not normalized_data.time_series:
            logger.warning("River Validation Failed: No station data found.")
            return False
            
        seen_metrics = set()
        for item in normalized_data.time_series:
            if not item.get("area_id") or not item.get("timestamp"):
                logger.warning(f"River Validation Failed: Missing fields: {item}")
                return False
                
            val = item.get("value")
            if val is None or not isinstance(val, (int, float)) or val < 0:
                logger.warning(f"River Validation Failed: Invalid measurement (negative/null): {item}")
                return False
                
            metric_id = f"{item['area_id']}_{item['parameter']}_{item['timestamp'].timestamp()}"
            if metric_id in seen_metrics:
                logger.warning(f"River Validation Failed: Duplicate observation: {metric_id}")
                return False
            seen_metrics.add(metric_id)
                
        return True
