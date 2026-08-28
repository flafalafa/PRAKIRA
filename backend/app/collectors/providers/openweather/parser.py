"""Parses OpenWeather raw payload into Python dictionaries."""
from app.collectors.providers.openweather.models import OpenWeatherParsedData
from app.collectors.providers.openweather.exceptions import OpenWeatherParsingError
from app.core.logger import get_logger

logger = get_logger(__name__)

class OpenWeatherParser:
    @staticmethod
    def parse_onecall(raw_json: dict) -> OpenWeatherParsedData:
        try:
            return OpenWeatherParsedData(
                lat=raw_json.get("lat", 0.0),
                lon=raw_json.get("lon", 0.0),
                timezone=raw_json.get("timezone", "UTC"),
                current=raw_json.get("current"),
                hourly=raw_json.get("hourly", []),
                daily=raw_json.get("daily", []),
                alerts=raw_json.get("alerts", [])
            )
        except Exception as e:
            logger.error(f"Failed to parse OpenWeather JSON: {str(e)}")
            raise OpenWeatherParsingError(f"JSON parsing failed: {str(e)}")
