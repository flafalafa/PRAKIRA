"""Weather Analysis Context."""
from dataclasses import dataclass, field
from typing import List, Dict, Any
from app.pipeline.canonical import CanonicalRecord

@dataclass(frozen=True)
class WeatherContext:
    analysis_id: str
    weather_observations: List[CanonicalRecord] = field(default_factory=list)
    rainfall_observations: List[CanonicalRecord] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
