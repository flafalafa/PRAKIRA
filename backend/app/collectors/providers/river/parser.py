"""Parses River raw payload into Python dictionaries."""
from app.collectors.providers.river.models import RiverParsedData, StationData
from app.collectors.providers.river.exceptions import RiverParsingError
from app.core.logger import get_logger

logger = get_logger(__name__)

class RiverParser:
    @staticmethod
    def parse_payload(raw_json: dict, provider_name: str) -> RiverParsedData:
        try:
            # Assuming a generic standard JSON response format across different providers.
            stations = []
            for item in raw_json.get("data", []):
                stations.append(StationData(
                    station_id=item.get("id", ""),
                    name=item.get("name", ""),
                    lat=float(item.get("latitude", 0.0)),
                    lon=float(item.get("longitude", 0.0)),
                    water_level=float(item.get("water_level", 0.0)),
                    flow_rate=float(item.get("flow_rate", 0.0)),
                    status=item.get("status", "UNKNOWN"),
                    timestamp=item.get("timestamp", "")
                ))
            return RiverParsedData(provider_name=provider_name, stations=stations)
        except Exception as e:
            logger.error(f"Failed to parse River JSON from {provider_name}: {str(e)}")
            raise RiverParsingError(f"JSON parsing failed: {str(e)}")
