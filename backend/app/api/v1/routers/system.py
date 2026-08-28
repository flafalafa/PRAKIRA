"""System Status Router."""
from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.api.v1.schemas.response import SuccessResponse
from app.api.v1.schemas.response import ApiMeta
from app.api.v1.dependencies import get_request_metadata

router = APIRouter(prefix="/system", tags=["System"])

@router.get("/info", response_model=SuccessResponse[Dict[str, str]])
async def system_info(meta: Dict[str, Any] = Depends(get_request_metadata)):
    return SuccessResponse(data={"version": "1.0.0", "environment": "production"}, request_id=meta["request_id"])
