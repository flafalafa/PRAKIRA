"""Standardized API Response Schemas."""
from typing import Generic, TypeVar, Optional, Any, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from app.api.v1.schemas.pagination import PaginationMeta

T = TypeVar('T')

class ApiMeta(BaseModel):
    pagination: Optional[PaginationMeta] = None
    source: Optional[str] = None
    last_updated: Optional[datetime] = None
    warnings: Optional[List[str]] = None
    
    model_config = {"extra": "allow"}

class SuccessResponse(BaseModel, Generic[T]):
    data: T
    meta: Optional[ApiMeta] = Field(default_factory=ApiMeta)
    request_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = "v1"

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    meta: ApiMeta
    request_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = "v1"
