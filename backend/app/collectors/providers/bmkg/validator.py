"""Validates the Canonical NormalizedData DTO for BMKG."""
from app.collectors.dto.normalized import NormalizedData
from app.core.logger import get_logger

logger = get_logger(__name__)

class BMKGValidator:
    @staticmethod
    def validate(normalized_data: NormalizedData) -> bool:
        if not normalized_data.time_series:
            logger.warning("BMKG Validation Failed: No time series data found.")
            return False
            
        # Check required fields in at least one time series item
        for item in normalized_data.time_series:
            if not item.get("area_id") or not item.get("timestamp"):
                logger.warning(f"BMKG Validation Failed: Missing required fields in time series item: {item}")
                return False
                
        return True
