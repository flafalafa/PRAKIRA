"""Radar Analysis Context."""
from dataclasses import dataclass, field
from typing import List, Dict, Any
from app.pipeline.canonical import CanonicalRecord

@dataclass(frozen=True)
class RadarContext:
    analysis_id: str
    radar_observations: List[CanonicalRecord] = field(default_factory=list)
    area_metadata: Dict[str, Any] = field(default_factory=dict)
