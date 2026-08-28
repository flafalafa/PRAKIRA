"""Area Mappers."""
from app.domain.entities.area import Area
from app.api.v1.schemas.area import AreaResponse
from app.api.v1.schemas.location import LocationResponse

class AreaMapper:
    @staticmethod
    def to_response(area: Area) -> AreaResponse:
        location = None
        if area.center_coordinate:
            location = LocationResponse(
                latitude=area.center_coordinate.latitude.value,
                longitude=area.center_coordinate.longitude.value,
            )
            
        return AreaResponse(
            area_id=area.id,
            area_name=area.name,
            area_code=area.code.value,
            status=area.status.value,
            area_type="CITY", # Fallback since Area doesn't have area_type
            location=location,
            created_at=area.created_at.value,
            updated_at=area.updated_at.value
        )
