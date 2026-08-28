"""Prepares mapping from Canonical DTO to Domain DTO."""
from app.collectors.dto.normalized import NormalizedData

class RiverMapper:
    @staticmethod
    def to_domain_dto(normalized_data: NormalizedData) -> dict:
        grouped_stations = {}
        for item in normalized_data.time_series or []:
            station_id = item['area_id']
            if station_id not in grouped_stations:
                grouped_stations[station_id] = {
                    "station_id": station_id,
                    "timestamp": item['timestamp'],
                    "metrics": {},
                    "metadata": item.get('metadata', {})
                }
            grouped_stations[station_id]["metrics"][item['parameter']] = item['value']
            
        return {
            "provider": normalized_data.provider_id,
            "observations": list(grouped_stations.values())
        }
