"""Alerts Router."""
from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, Optional
from datetime import datetime
from app.api.v1.schemas.response import SuccessResponse, PaginatedResponse
from app.api.v1.schemas.response import ApiMeta
from app.api.v1.schemas.alert import AlertResponse, AlertDetailResponse, AlertFilterParams
from app.api.v1.dependencies import get_request_metadata
from app.api.v1.dependencies.notification import get_alert_service
from app.api.v1.services.alert_service import AlertApplicationService
from app.api.v1.mappers.alert_mapper import AlertMapper
from app.api.security.dependencies import get_current_user
from app.api.security.context import SecurityContext
from app.core.logger import get_logger
from app.api.v1.dependencies.area import get_area_service
from app.api.v1.services.area_service import AreaApplicationService
from app.api.v1.schemas.notification import NotificationDeliveryStatus

logger = get_logger(__name__)

router = APIRouter(tags=["Alerts"])

# Sub-router included in areas router
area_alerts_router = APIRouter(tags=["Alerts"])

@area_alerts_router.get("/{area_id}/alerts/active", response_model=SuccessResponse[AlertResponse])
async def get_active_alert(
    area_id: str,
    alert_service: AlertApplicationService = Depends(get_alert_service),
    area_service: AreaApplicationService = Depends(get_area_service),
    meta: Dict[str, Any] = Depends(get_request_metadata),
    user: SecurityContext = Depends(get_current_user)
):
    logger.info(f"Active alert for {area_id} requested by {user.principal_id}")
    await area_service.get_area(area_id)
    alert = await alert_service.get_active_alert(area_id)
    
    response_data = AlertMapper.to_response(alert)
    return SuccessResponse(data=response_data, request_id=meta["request_id"])

@area_alerts_router.get("/{area_id}/alerts", response_model=PaginatedResponse[AlertResponse])
async def list_alerts(
    area_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    alert_service: AlertApplicationService = Depends(get_alert_service),
    area_service: AreaApplicationService = Depends(get_area_service),
    meta: Dict[str, Any] = Depends(get_request_metadata),
    user: SecurityContext = Depends(get_current_user)
):
    logger.info(f"Alert history for {area_id} requested by {user.principal_id}")
    await area_service.get_area(area_id)
    
    filters = AlertFilterParams(
        page=page, page_size=page_size, from_date=from_date,
        to_date=to_date, severity=severity, status=status
    )
    
    alerts, pagination = await alert_service.list_alerts(area_id, filters)
    response_data = [AlertMapper.to_response(a) for a in alerts]
    
    return PaginatedResponse(data=response_data, meta=ApiMeta(pagination=pagination), request_id=meta["request_id"])

# Independent router for /alerts/...
@router.get("/alerts/{alert_id}", response_model=SuccessResponse[AlertDetailResponse])
async def get_alert_detail(
    alert_id: str,
    alert_service: AlertApplicationService = Depends(get_alert_service),
    meta: Dict[str, Any] = Depends(get_request_metadata),
    user: SecurityContext = Depends(get_current_user)
):
    logger.info(f"Get alert {alert_id} requested by {user.principal_id}")
    alert = await alert_service.get_alert(alert_id)
    response_data = AlertMapper.to_detail_response(alert)
    
    return SuccessResponse(data=response_data, request_id=meta["request_id"])

@router.get("/alerts/{alert_id}/status", response_model=SuccessResponse[NotificationDeliveryStatus])
async def get_alert_delivery_status(
    alert_id: str,
    alert_service: AlertApplicationService = Depends(get_alert_service),
    meta: Dict[str, Any] = Depends(get_request_metadata),
    user: SecurityContext = Depends(get_current_user)
):
    logger.info(f"Delivery status for alert {alert_id} requested by {user.principal_id}")
    alert = await alert_service.get_alert(alert_id)
    
    # Mocking delivery status extraction
    status = NotificationDeliveryStatus(
        notification_status="DELIVERED",
        provider_status="SUCCESS",
        delivery_timestamp=getattr(alert, "updated_at", None)
    )
    
    return SuccessResponse(data=status, request_id=meta["request_id"])
