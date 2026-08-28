"""Notifications Router."""
from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, Optional
from datetime import datetime
from app.api.v1.schemas.response import SuccessResponse, PaginatedResponse
from app.api.v1.schemas.response import ApiMeta
from app.api.v1.schemas.notification import NotificationResponse, NotificationFilterParams
from app.api.v1.dependencies import get_request_metadata
from app.api.v1.dependencies.notification import get_notification_service
from app.api.v1.services.notification_service import NotificationApplicationService
from app.api.v1.mappers.notification_mapper import NotificationMapper
from app.api.security.dependencies import get_current_user
from app.api.security.context import SecurityContext
from app.core.logger import get_logger
from app.api.v1.dependencies.area import get_area_service
from app.api.v1.services.area_service import AreaApplicationService

logger = get_logger(__name__)

router = APIRouter(tags=["Notifications"])
area_notifications_router = APIRouter(tags=["Notifications"])

@area_notifications_router.get("/{area_id}/notifications", response_model=PaginatedResponse[NotificationResponse])
async def list_notifications(
    area_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    provider: Optional[str] = Query(None),
    notif_service: NotificationApplicationService = Depends(get_notification_service),
    area_service: AreaApplicationService = Depends(get_area_service),
    meta: Dict[str, Any] = Depends(get_request_metadata),
    user: SecurityContext = Depends(get_current_user)
):
    logger.info(f"Notification history for {area_id} requested by {user.principal_id}")
    await area_service.get_area(area_id)
    
    filters = NotificationFilterParams(
        page=page, page_size=page_size, from_date=from_date,
        to_date=to_date, severity=severity, status=status, provider=provider
    )
    
    notifications, pagination = await notif_service.list_notifications(area_id, filters, user.principal_id)
    response_data = [NotificationMapper.to_response(n) for n in notifications]
    
    return PaginatedResponse(data=response_data, meta=ApiMeta(pagination=pagination), request_id=meta["request_id"])

@router.get("/notifications/{notification_id}", response_model=SuccessResponse[NotificationResponse])
async def get_notification_detail(
    notification_id: str,
    notif_service: NotificationApplicationService = Depends(get_notification_service),
    meta: Dict[str, Any] = Depends(get_request_metadata),
    user: SecurityContext = Depends(get_current_user)
):
    logger.info(f"Get notification {notification_id} requested by {user.principal_id}")
    notification = await notif_service.get_notification(notification_id, user.principal_id)
    response_data = NotificationMapper.to_response(notification)
    
    return SuccessResponse(data=response_data, request_id=meta["request_id"])
