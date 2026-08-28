"""Prepares mapping from Canonical DTO to Domain DTO."""
from app.collectors.dto.normalized import NormalizedData

class OpenWeatherMapper:
    @staticmethod
    def to_domain_dto(normalized_data: NormalizedData) -> dict:
        grouped_data = {}
        for item in normalized_data.time_series or []:
            key = f"{item['area_id']}_{item['timestamp'].isoformat()}"
            if key not in grouped_data:
                grouped_data[key] = {
                    "area_id": item['area_id'],
                    "timestamp": item['timestamp'],
                    "metrics": {}
                }
            grouped_data[key]["metrics"][item['parameter']] = item['value']
            
        return {
            "provider": normalized_data.provider_id,
            "location": normalized_data.location_data,
            "observations": list(grouped_data.values())
        }
