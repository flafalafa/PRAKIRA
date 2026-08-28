"""Flood Status Router."""
from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, Optional
from datetime import datetime
from app.api.v1.schemas.response import SuccessResponse, PaginatedResponse
from app.api.v1.schemas.response import ApiMeta
from app.api.v1.schemas.flood_status import FloodStatusResponse
from app.api.v1.schemas.prediction import PredictionResponse, PredictionSummaryResponse, PredictionHistoryFilterParams
from app.api.v1.dependencies import get_request_metadata
from app.api.v1.dependencies.prediction import get_prediction_service
from app.api.v1.dependencies.area import get_area_service
from app.api.v1.services.prediction_service import PredictionApplicationService
from app.api.v1.services.area_service import AreaApplicationService
from app.api.v1.mappers.prediction_mapper import PredictionMapper
from app.api.security.dependencies import get_current_user
from app.api.security.context import SecurityContext
from app.core.logger import get_logger

logger = get_logger(__name__)

# Note: The design calls for GET /api/v1/areas/{area_id}/flood-status, etc. 
# We'll attach these to a sub-router that gets included in areas.py, or define them here
# For clean structure, we'll expose a router that should be included with prefix="/areas/{area_id}"

router = APIRouter(tags=["Flood Status"])

@router.get("/{area_id}/flood-status", response_model=SuccessResponse[FloodStatusResponse])
async def get_flood_status(
    area_id: str,
    pred_service: PredictionApplicationService = Depends(get_prediction_service),
    area_service: AreaApplicationService = Depends(get_area_service),
    meta: Dict[str, Any] = Depends(get_request_metadata),
    user: SecurityContext = Depends(get_current_user)
):
    logger.info(f"Flood status for {area_id} requested by {user.principal_id}")
    area = await area_service.get_area(area_id)
    prediction = await pred_service.get_current_prediction(area_id)
    
    response_data = PredictionMapper.to_flood_status(prediction, area.name)
    
    return SuccessResponse(data=response_data, request_id=meta["request_id"])

@router.get("/{area_id}/prediction", response_model=SuccessResponse[PredictionResponse])
async def get_current_prediction(
    area_id: str,
    pred_service: PredictionApplicationService = Depends(get_prediction_service),
    area_service: AreaApplicationService = Depends(get_area_service), # Just to validate area exists
    meta: Dict[str, Any] = Depends(get_request_metadata),
    user: SecurityContext = Depends(get_current_user)
):
    logger.info(f"Current prediction for {area_id} requested by {user.principal_id}")
    await area_service.get_area(area_id) # Validates area exists
    prediction = await pred_service.get_current_prediction(area_id)
    
    response_data = PredictionMapper.to_response(prediction)
    
    return SuccessResponse(data=response_data, request_id=meta["request_id"])

@router.get("/{area_id}/predictions", response_model=PaginatedResponse[PredictionSummaryResponse])
async def list_prediction_history(
    area_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    risk_level: Optional[str] = Query(None),
    prediction_status: Optional[str] = Query(None),
    pred_service: PredictionApplicationService = Depends(get_prediction_service),
    area_service: AreaApplicationService = Depends(get_area_service),
    meta: Dict[str, Any] = Depends(get_request_metadata),
    user: SecurityContext = Depends(get_current_user)
):
    logger.info(f"Prediction history for {area_id} requested by {user.principal_id}")
    await area_service.get_area(area_id)
    
    filters = PredictionHistoryFilterParams(
        page=page, page_size=page_size, from_date=from_date,
        to_date=to_date, risk_level=risk_level, prediction_status=prediction_status
    )
    
    predictions, pagination = await pred_service.list_prediction_history(area_id, filters)
    response_data = [PredictionMapper.to_summary_response(p) for p in predictions]
    
    return PaginatedResponse(data=response_data, meta=ApiMeta(pagination=pagination), request_id=meta["request_id"])
