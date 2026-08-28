"""Risk Assessment Context."""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from app.decision.weather.result import WeatherAnalysisResult
from app.decision.hydrology.result import HydrologyAnalysisResult
from app.decision.radar.result import RadarAnalysisResult

@dataclass(frozen=True)
class RiskContext:
    assessment_id: str
    weather_result: Optional[WeatherAnalysisResult] = None
    hydrology_result: Optional[HydrologyAnalysisResult] = None
    radar_result: Optional[RadarAnalysisResult] = None
    area_metadata: Dict[str, Any] = field(default_factory=dict)
    historical_metadata: Dict[str, Any] = field(default_factory=dict)
