"""Prediction Router."""
from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.api.v1.schemas.response import SuccessResponse
from app.api.v1.schemas.response import ApiMeta
from app.api.v1.schemas.prediction import PredictionResponse
from app.api.v1.dependencies import get_request_metadata
from app.api.v1.dependencies.prediction import get_prediction_service
from app.api.v1.services.prediction_service import PredictionApplicationService
from app.api.v1.mappers.prediction_mapper import PredictionMapper
from app.api.security.dependencies import get_current_user
from app.api.security.context import SecurityContext
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/predictions", tags=["Predictions"])

@router.get("/{prediction_id}", response_model=SuccessResponse[PredictionResponse])
async def get_prediction_detail(
    prediction_id: str,
    service: PredictionApplicationService = Depends(get_prediction_service),
    meta: Dict[str, Any] = Depends(get_request_metadata),
    user: SecurityContext = Depends(get_current_user)
):
    logger.info(f"Get prediction {prediction_id} requested by {user.principal_id}")
    prediction = await service.get_prediction_by_id(prediction_id)
    response_data = PredictionMapper.to_response(prediction)
    
    return SuccessResponse(data=response_data, request_id=meta["request_id"])
