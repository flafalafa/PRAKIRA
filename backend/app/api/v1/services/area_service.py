"""Area Application Service."""
from typing import List, Tuple
from app.domain.interfaces.area_repository import IAreaRepository as AreaRepository
from app.domain.entities.area import Area
from app.api.v1.schemas.area_filters import AreaFilterParams
from app.api.v1.schemas.pagination import PaginationMeta
from app.exceptions.not_found import NotFoundException

class AreaApplicationService:
    def __init__(self, repository: AreaRepository):
        self.repository = repository
        
    async def get_area(self, area_id: str) -> Area:
        area = await self.repository.find_by_id(area_id)
        if not area:
            raise NotFoundException(f"Area {area_id} not found")
        return area
        
    async def list_areas(self, filters: AreaFilterParams) -> Tuple[List[Area], PaginationMeta]:
        areas = await self.repository.list()
        
        if filters.status:
            areas = [a for a in areas if a.status.value == filters.status]
            
        if filters.search:
            search_term = filters.search.lower()
            areas = [a for a in areas if search_term in a.name.lower() or search_term in a.code.lower()]
            
        total = len(areas)
        start = (filters.page - 1) * filters.page_size
        end = start + filters.page_size
        paginated_areas = areas[start:end]
        
        total_pages = max(1, (total + filters.page_size - 1) // filters.page_size)
        
        pagination = PaginationMeta(
            page=filters.page,
            page_size=filters.page_size,
            total=total,
            total_pages=total_pages,
            has_next=filters.page < total_pages,
            has_previous=filters.page > 1
        )
        
        return paginated_areas, pagination
