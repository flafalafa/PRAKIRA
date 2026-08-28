"""Orchestrator Context."""
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class OrchestratorContext:
    workflow_id: str
    weather_observations: list = field(default_factory=list)
    rainfall_observations: list = field(default_factory=list)
    river_observations: list = field(default_factory=list)
    radar_observations: list = field(default_factory=list)
    area_metadata: Dict[str, Any] = field(default_factory=dict)
    historical_metadata: Dict[str, Any] = field(default_factory=dict)
