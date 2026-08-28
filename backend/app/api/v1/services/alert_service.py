"""Alert Application Service."""
from typing import List, Tuple, Any
from app.api.v1.schemas.alert import AlertFilterParams
from app.api.v1.schemas.pagination import PaginationMeta
from app.exceptions.not_found import NotFoundException

class AlertApplicationService:
    def __init__(self, repository: Any):
        self.repository = repository
        
    async def get_active_alert(self, area_id: str) -> Any:
        alert = await self.repository.get_active_for_area(area_id)
        if not alert:
            raise NotFoundException(f"No active alert found for area {area_id}")
        return alert
        
    async def get_alert(self, alert_id: str) -> Any:
        alert = await self.repository.get_by_id(alert_id)
        if not alert:
            raise NotFoundException(f"Alert {alert_id} not found")
        return alert
        
    async def list_alerts(self, area_id: str, filters: AlertFilterParams) -> Tuple[List[Any], PaginationMeta]:
        alerts = await self.repository.list_by_area(area_id)
        
        # Stub logic for filtering
        if filters.severity:
            alerts = [a for a in alerts if getattr(a, "level", None) == filters.severity]
        if filters.status:
            alerts = [a for a in alerts if getattr(a, "status", None) == filters.status]
            
        total = len(alerts)
        start = (filters.page - 1) * filters.page_size
        end = start + filters.page_size
        paginated = alerts[start:end]
        
        total_pages = max(1, (total + filters.page_size - 1) // filters.page_size)
        
        pagination = PaginationMeta(
            page=filters.page,
            page_size=filters.page_size,
            total=total,
            total_pages=total_pages,
            has_next=filters.page < total_pages,
            has_previous=filters.page > 1
        )
        
        return paginated, pagination
