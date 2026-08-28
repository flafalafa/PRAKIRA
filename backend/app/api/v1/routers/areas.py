"""Area Router."""
from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, Optional
from app.api.v1.schemas.response import SuccessResponse, PaginatedResponse
from app.api.v1.schemas.response import ApiMeta
from app.api.v1.schemas.area import AreaResponse
from app.api.v1.schemas.location import LocationResponse
from app.api.v1.schemas.area_filters import AreaFilterParams
from app.api.v1.dependencies import get_request_metadata
from app.api.v1.dependencies.area import get_area_service
from app.api.v1.services.area_service import AreaApplicationService
from app.api.v1.mappers.area_mapper import AreaMapper
from app.api.security.dependencies import get_current_user
from app.api.security.context import SecurityContext
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/areas", tags=["Areas"])

@router.get("", response_model=PaginatedResponse[AreaResponse])
async def list_areas(
    status: Optional[str] = Query(None),
    active: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    area_type: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: AreaApplicationService = Depends(get_area_service),
    meta: Dict[str, Any] = Depends(get_request_metadata),
    user: SecurityContext = Depends(get_current_user)
):
    logger.info(f"Listing areas requested by {user.principal_id}")
    filters = AreaFilterParams(
        status=status, active=active, search=search, 
        area_type=area_type, page=page, page_size=page_size
    )
    
    areas, pagination = await service.list_areas(filters)
    area_responses = [AreaMapper.to_response(a) for a in areas]
    
    return PaginatedResponse(data=area_responses, meta=ApiMeta(pagination=pagination), request_id=meta["request_id"])

@router.get("/{area_id}", response_model=SuccessResponse[AreaResponse])
async def get_area(
    area_id: str,
    service: AreaApplicationService = Depends(get_area_service),
    meta: Dict[str, Any] = Depends(get_request_metadata),
    user: SecurityContext = Depends(get_current_user)
):
    logger.info(f"Get area {area_id} requested by {user.principal_id}")
    area = await service.get_area(area_id)
    response_data = AreaMapper.to_response(area)
    
    return SuccessResponse(data=response_data, request_id=meta["request_id"])

@router.get("/{area_id}/location", response_model=SuccessResponse[LocationResponse])
async def get_area_location(
    area_id: str,
    service: AreaApplicationService = Depends(get_area_service),
    meta: Dict[str, Any] = Depends(get_request_metadata),
    user: SecurityContext = Depends(get_current_user)
):
    logger.info(f"Get area location {area_id} requested by {user.principal_id}")
    area = await service.get_area(area_id)
    
    if not area.center_coordinate:
        location = LocationResponse(latitude=0.0, longitude=0.0)
    else:
        location = LocationResponse(
            latitude=area.center_coordinate.latitude.value,
            longitude=area.center_coordinate.longitude.value,
        )
        
    return SuccessResponse(data=location, request_id=meta["request_id"])
