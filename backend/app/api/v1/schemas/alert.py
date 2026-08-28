"""Alert API Schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AlertResponse(BaseModel):
    alert_id: str
    area_id: str
    alert_level: str
    risk_score: float
    confidence: Optional[float] = None
    prediction_id: str
    title: str
    message: str
    recommendation: Optional[str] = None
    issued_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None
    estimated_arrival_time: Optional[datetime] = None
    alert_status: str

class AlertExplanation(BaseModel):
    primary_risk_factors: List[str] = Field(default_factory=list)
    supporting_observations: List[str] = Field(default_factory=list)
    triggered_rules: List[str] = Field(default_factory=list)
    confidence_explanation: str = ""
    missing_data: List[str] = Field(default_factory=list)

class AlertDetailResponse(AlertResponse):
    explanation: Optional[AlertExplanation] = None

class AlertFilterParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    severity: Optional[str] = None
    status: Optional[str] = None
