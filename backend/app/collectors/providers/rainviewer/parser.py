"""Parses RainViewer raw payload into Python dictionaries."""
from app.collectors.providers.rainviewer.models import RainViewerParsedData
from app.collectors.providers.rainviewer.exceptions import RainViewerParsingError
from app.core.logger import get_logger

logger = get_logger(__name__)

class RainViewerParser:
    @staticmethod
    def parse_maps(raw_json: dict) -> RainViewerParsedData:
        try:
            return RainViewerParsedData(
                version=raw_json.get("version", ""),
                generated=raw_json.get("generated", 0),
                host=raw_json.get("host", ""),
                radar=raw_json.get("radar", {}),
                satellite=raw_json.get("satellite", {})
            )
        except Exception as e:
            logger.error(f"Failed to parse RainViewer JSON: {str(e)}")
            raise RainViewerParsingError(f"JSON parsing failed: {str(e)}")
