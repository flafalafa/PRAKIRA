"""Prediction API Schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class PredictionExplanation(BaseModel):
    primary_risk_factors: List[str] = Field(default_factory=list)
    supporting_observations: List[str] = Field(default_factory=list)
    triggered_rules: List[str] = Field(default_factory=list)
    confidence_explanation: str = ""
    missing_data: List[str] = Field(default_factory=list)
    reason_summary: str = ""

class PredictionResponse(BaseModel):
    prediction_id: str
    area_id: str
    prediction_time: datetime
    risk_score: float
    risk_level: str
    confidence: Optional[float] = None
    prediction_status: str
    estimated_arrival_time: Optional[datetime] = None
    estimated_flood_depth: Optional[float] = None
    estimated_duration: Optional[int] = None
    recommendation: Optional[str] = None
    explanation: Optional[PredictionExplanation] = None
    supporting_factors: Dict[str, Any] = Field(default_factory=dict)
    prediction_version: str = "1.0"
    created_at: datetime

class PredictionSummaryResponse(BaseModel):
    prediction_id: str
    area_id: str
    prediction_time: datetime
    risk_score: float
    risk_level: str
    prediction_status: str
    created_at: datetime
    
class PredictionHistoryFilterParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    risk_level: Optional[str] = None
    prediction_status: Optional[str] = None
