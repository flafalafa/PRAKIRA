"""Prepares mapping from Canonical DTO to Domain DTO. Does not instantiate Domain Entities."""
from app.collectors.dto.normalized import NormalizedData

class BMKGMapper:
    @staticmethod
    def to_domain_dto(normalized_data: NormalizedData) -> dict:
        """
        Maps Canonical NormalizedData to a dictionary structure ready 
        for Domain Entity instantiation by the Application Service.
        """
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
            "observations": list(grouped_data.values())
        }
