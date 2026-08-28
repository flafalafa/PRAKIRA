"""Radar Analysis Rules."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.decision.radar.context import RadarContext

class BaseRadarRule(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    async def evaluate(self, context: RadarContext, analysis_data: Dict[str, Any]) -> bool:
        pass

class StormApproachingRule(BaseRadarRule):
    name = "STORM_APPROACHING"
    async def evaluate(self, context: RadarContext, analysis_data: Dict[str, Any]) -> bool:
        eta = analysis_data.get("eta")
        return eta is not None and eta <= 60

class RapidCellGrowthRule(BaseRadarRule):
    name = "RAPID_CELL_GROWTH"
    async def evaluate(self, context: RadarContext, analysis_data: Dict[str, Any]) -> bool:
        tracking = analysis_data.get("tracking", {})
        return tracking.get("growth_trend") == "EXPANDING" and tracking.get("intensity_trend") == "INCREASING"
