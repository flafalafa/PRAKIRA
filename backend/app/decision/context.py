"""Decision Context for the Flood Decision Engine."""
from dataclasses import dataclass, field
from typing import List, Dict, Any
from app.pipeline.canonical import CanonicalRecord

@dataclass(frozen=True)
class DecisionContext:
    """
    Aggregates all observations needed during one evaluation cycle.
    Must remain immutable throughout the decision execution.
    """
    context_id: str
    weather_observations: List[CanonicalRecord] = field(default_factory=list)
    rainfall_observations: List[CanonicalRecord] = field(default_factory=list)
    river_observations: List[CanonicalRecord] = field(default_factory=list)
    radar_observations: List[CanonicalRecord] = field(default_factory=list)
    area_metadata: Dict[str, Any] = field(default_factory=dict)
