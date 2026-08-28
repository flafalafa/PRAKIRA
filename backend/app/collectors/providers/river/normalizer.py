"""Normalizes River Parsed Data into Canonical NormalizedData DTO."""
from datetime import datetime, timezone
from app.collectors.providers.river.models import RiverParsedData
from app.collectors.dto.normalized import NormalizedData
from app.core.logger import get_logger

logger = get_logger(__name__)

class RiverNormalizer:
    @staticmethod
    def normalize(parsed_data: RiverParsedData) -> NormalizedData:
        logger.debug(f"Normalization Started for River data ({parsed_data.provider_name}).")
        
        time_series = []
        
        for station in parsed_data.stations:
            try:
                dt = datetime.fromisoformat(station.timestamp.replace("Z", "+00:00"))
            except ValueError:
                dt = datetime.utcnow().replace(tzinfo=timezone.utc)
                
            metadata = {
                "station_name": station.name,
                "status": station.status,
                "lat": station.lat,
                "lon": station.lon
            }
            
            time_series.append({
                "area_id": f"river_station_{station.station_id}",
                "timestamp": dt,
                "parameter": "water_level",
                "value": station.water_level,
                "metadata": metadata
            })
            
            time_series.append({
                "area_id": f"river_station_{station.station_id}",
                "timestamp": dt,
                "parameter": "flow_rate",
                "value": station.flow_rate,
                "metadata": metadata
            })
            
        return NormalizedData(
            provider_id=f"RiverTelemetry_{parsed_data.provider_name}",
            normalized_time=datetime.now(timezone.utc),
            time_series=time_series
        )
