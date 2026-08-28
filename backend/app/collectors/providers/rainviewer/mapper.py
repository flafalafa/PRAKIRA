"""Prepares mapping from Canonical Radar DTO to Domain DTO."""
from app.collectors.dto.normalized import NormalizedData

class RainViewerMapper:
    @staticmethod
    def to_domain_dto(normalized_data: NormalizedData) -> dict:
        frames = []
        for item in normalized_data.time_series or []:
            frames.append({
                "timestamp": item['timestamp'],
                "type": item['parameter'],
                "url": item['value'],
                "metadata": item.get('metadata', {})
            })
            
        # Sort frames by time chronologically
        frames.sort(key=lambda x: x["timestamp"])
        
        return {
            "provider": normalized_data.provider_id,
            "coverage": normalized_data.location_data,
            "radar_frames": frames
        }
