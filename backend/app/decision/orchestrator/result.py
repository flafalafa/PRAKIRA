"""Orchestrator Result Data Models."""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.decision.orchestrator.state import WorkflowState
from app.decision.weather.result import WeatherAnalysisResult
from app.decision.hydrology.result import HydrologyAnalysisResult
from app.decision.radar.result import RadarAnalysisResult
from app.decision.risk.result import FloodRiskAssessmentResult

class OrchestratorResult(BaseModel):
    workflow_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    state: WorkflowState = WorkflowState.CREATED
    execution_duration_ms: int = 0
    weather_result: Optional[WeatherAnalysisResult] = None
    hydrology_result: Optional[HydrologyAnalysisResult] = None
    radar_result: Optional[RadarAnalysisResult] = None
    risk_result: Optional[FloodRiskAssessmentResult] = None
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    execution_metadata: Dict[str, Any] = Field(default_factory=dict)
