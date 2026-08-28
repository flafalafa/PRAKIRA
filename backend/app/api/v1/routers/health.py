"""Health Check Router."""
from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.api.v1.schemas.response import SuccessResponse
from app.api.v1.schemas.response import ApiMeta
from app.api.v1.dependencies import get_request_metadata

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=SuccessResponse[Dict[str, str]])
async def health_check(meta: Dict[str, Any] = Depends(get_request_metadata)):
    return SuccessResponse(data={"status": "OK", "service": "Flood Guardian API"}, request_id=meta["request_id"])
