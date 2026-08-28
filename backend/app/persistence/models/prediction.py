from sqlalchemy import Column, String, Float, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB
from app.entities.base import BaseEntity
from app.entities.mixins import TimestampMixin
from app.domain.entities.flood_prediction import RiskLevel, PredictionStatus
from datetime import datetime, timezone

class FloodPredictionModel(BaseEntity, TimestampMixin):
    __tablename__ = "flood_predictions"

    id = Column(String(36), primary_key=True)
    prediction_code = Column(String(50), nullable=False, unique=True, index=True)
    area_id = Column(String(36), nullable=False, index=True)
    river_id = Column(String(36), nullable=True)
    
    # Core prediction timestamps
    prediction_time = Column(DateTime(timezone=True), nullable=False, index=True)
    forecast_start = Column(DateTime(timezone=True), nullable=False)
    forecast_end = Column(DateTime(timezone=True), nullable=False)
    
    # Methodology
    prediction_source = Column(String(100), nullable=False)
    prediction_method = Column(String(100), nullable=False)
    
    # Scores and Probabilities
    risk_score = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    flood_probability = Column(Float, nullable=True)
    
    # Impact estimates
    estimated_flood_depth = Column(Float, nullable=True)
    estimated_arrival_time = Column(DateTime(timezone=True), nullable=True)
    expected_duration_seconds = Column(Float, nullable=True)
    
    # References
    rainfall_reference = Column(String(100), nullable=True)
    river_reference = Column(String(100), nullable=True)
    weather_reference = Column(String(100), nullable=True)
    
    # Outcomes
    recommended_action = Column(String(500), nullable=False)
    risk_level = Column(SAEnum(RiskLevel, name="risklevel"), nullable=False, default=RiskLevel.VERY_LOW)
    status = Column(SAEnum(PredictionStatus, name="predictionstatus"), nullable=False, default=PredictionStatus.DRAFT)
