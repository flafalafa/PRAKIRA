"""Validates the Canonical NormalizedData DTO for OpenWeather."""
from app.collectors.dto.normalized import NormalizedData
from app.core.logger import get_logger

logger = get_logger(__name__)

class OpenWeatherValidator:
    @staticmethod
    def validate(normalized_data: NormalizedData) -> bool:
        if not normalized_data.time_series:
            logger.warning("OpenWeather Validation Failed: No time series data.")
            return False
            
        for item in normalized_data.time_series:
            if not item.get("area_id") or not item.get("timestamp"):
                logger.warning(f"OpenWeather Validation Failed: Missing required fields in time series: {item}")
                return False
                
        return True
