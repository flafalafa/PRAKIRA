"""Notification Application Service."""
from typing import List, Tuple, Any
from app.api.v1.schemas.notification import NotificationFilterParams
from app.api.v1.schemas.pagination import PaginationMeta
from app.exceptions.not_found import NotFoundException
from app.exceptions.authorization import AuthorizationException

class NotificationApplicationService:
    def __init__(self, repository: Any):
        self.repository = repository
        
    async def get_notification(self, notification_id: str, user_id: str) -> Any:
        notification = await self.repository.get_by_id(notification_id)
        if not notification:
            raise NotFoundException(f"Notification {notification_id} not found")
            
        # Security: User visibility check
        if getattr(notification, "user_id", None) and getattr(notification, "user_id") != user_id:
            raise AuthorizationException("Not authorized to view this notification")
            
        return notification
        
    async def list_notifications(self, area_id: str, filters: NotificationFilterParams, user_id: str) -> Tuple[List[Any], PaginationMeta]:
        notifications = await self.repository.list_by_area_and_user(area_id, user_id)
        
        total = len(notifications)
        start = (filters.page - 1) * filters.page_size
        end = start + filters.page_size
        paginated = notifications[start:end]
        
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
