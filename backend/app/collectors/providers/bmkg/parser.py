"""Parses BMKG raw payload into Python dictionaries."""
import json
from app.collectors.providers.bmkg.models import BMKGParsedData
from app.collectors.providers.bmkg.exceptions import BMKGParsingError
from app.core.logger import get_logger

logger = get_logger(__name__)

class BMKGParser:
    @staticmethod
    def parse_data(raw_data: str) -> BMKGParsedData:
        try:
            parsed = json.loads(raw_data)
            
            if "lokasi" not in parsed or "data" not in parsed:
                raise BMKGParsingError("Missing 'lokasi' or 'data' in BMKG JSON response.")
                
            return BMKGParsedData(
                lokasi=parsed["lokasi"],
                data=parsed["data"]
            )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse BMKG JSON: {str(e)}")
            raise BMKGParsingError(f"JSON parsing failed: {str(e)}")

