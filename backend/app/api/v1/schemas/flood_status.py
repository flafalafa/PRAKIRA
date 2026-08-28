"""Flood Status API Schemas."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FloodStatusResponse(BaseModel):
    area_id: str
    area_name: str
    current_risk_level: str
    risk_score: float
    confidence: Optional[float] = None
    prediction_status: str
    last_updated: datetime
    prediction_timestamp: datetime
    estimated_arrival_time: Optional[datetime] = None
    primary_risk_factor: Optional[str] = None
    recommended_action: Optional[str] = None
