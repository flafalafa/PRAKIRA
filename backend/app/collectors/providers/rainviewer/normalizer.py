"""Normalizes RainViewer Parsed Data into Canonical Radar DTO."""
from datetime import datetime, timezone
from app.collectors.providers.rainviewer.models import RainViewerParsedData
from app.collectors.dto.normalized import NormalizedData
from app.core.logger import get_logger

logger = get_logger(__name__)

class RainViewerNormalizer:
    @staticmethod
    def normalize(parsed_data: RainViewerParsedData) -> NormalizedData:
        logger.debug("Normalization Started for RainViewer data.")
        
        time_series = []
        host = parsed_data.host
        
        # Process past radar frames
        for frame in parsed_data.radar.get("past", []):
            dt = datetime.fromtimestamp(frame.get("time", 0), tz=timezone.utc)
            path = frame.get("path", "")
            # Canonical format for radar info
            time_series.append({
                "area_id": "global",
                "timestamp": dt,
                "parameter": "radar_frame_past",
                "value": f"{host}{path}",
                "metadata": {
                    "source": "RainViewer",
                    "frame_type": "past",
                    "resolution": 256 # Default RV tile size
                }
            })
            
        # Process nowcast radar frames
        for frame in parsed_data.radar.get("nowcast", []):
            dt = datetime.fromtimestamp(frame.get("time", 0), tz=timezone.utc)
            path = frame.get("path", "")
            time_series.append({
                "area_id": "global",
                "timestamp": dt,
                "parameter": "radar_frame_nowcast",
                "value": f"{host}{path}",
                "metadata": {
                    "source": "RainViewer",
                    "frame_type": "nowcast",
                    "resolution": 256
                }
            })
            
        return NormalizedData(
            provider_id="RainViewer",
            normalized_time=datetime.now(timezone.utc),
            time_series=time_series,
            location_data={"spatial_reference": "global"}
        )
