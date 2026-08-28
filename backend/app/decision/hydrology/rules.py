"""Hydrology Analysis Rules."""
from abc import ABC, abstractmethod
from typing import List
from app.decision.hydrology.context import HydrologyContext
from app.decision.hydrology.metrics import HydrologyMetrics

class BaseHydrologyRule(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    async def evaluate(self, context: HydrologyContext) -> bool:
        pass

class RapidWaterRiseRule(BaseHydrologyRule):
    name = "RAPID_WATER_RISE"
    async def evaluate(self, context: HydrologyContext) -> bool:
        rise_rate = HydrologyMetrics.calculate_rise_rate(context.river_observations)
        return rise_rate > 50.0
        
class HighCapacityUsageRule(BaseHydrologyRule):
    name = "HIGH_CAPACITY_USAGE"
    async def evaluate(self, context: HydrologyContext) -> bool:
        current_level = HydrologyMetrics.get_latest_water_level(context.river_observations)
        max_cap = context.river_metadata.get("max_capacity_cm", 300.0)
        usage = HydrologyMetrics.calculate_capacity_usage(current_level, max_cap)
        return usage > 90.0
