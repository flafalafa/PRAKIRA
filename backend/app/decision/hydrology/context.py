"""Hydrology Analysis Context."""
from dataclasses import dataclass, field
from typing import List, Dict, Any
from app.pipeline.canonical import CanonicalRecord

@dataclass(frozen=True)
class HydrologyContext:
    analysis_id: str
    river_observations: List[CanonicalRecord] = field(default_factory=list)
    area_metadata: Dict[str, Any] = field(default_factory=dict)
    river_metadata: Dict[str, Any] = field(default_factory=dict)
