"""Hydrology Metrics Calculator."""
from typing import List
from app.decision.hydrology.context import HydrologyContext
from app.pipeline.canonical import CanonicalRecord

class HydrologyMetrics:
    @staticmethod
    def _extract_values(records: List[CanonicalRecord], param_name: str) -> List[float]:
        vals = []
        for r in records:
            for m in r.measurements:
                if m.parameter.lower() == param_name.lower():
                    vals.append(m.value)
        return vals

    @staticmethod
    def get_latest_water_level(records: List[CanonicalRecord]) -> float:
        vals = HydrologyMetrics._extract_values(records, "water_level")
        return vals[-1] if vals else 0.0

    @staticmethod
    def calculate_average_water_level(records: List[CanonicalRecord]) -> float:
        vals = HydrologyMetrics._extract_values(records, "water_level")
        return sum(vals) / len(vals) if vals else 0.0

    @staticmethod
    def calculate_rise_rate(records: List[CanonicalRecord]) -> float:
        vals = HydrologyMetrics._extract_values(records, "water_level")
        if len(vals) < 2:
            return 0.0
        return vals[-1] - vals[0]

    @staticmethod
    def get_latest_flow_rate(records: List[CanonicalRecord]) -> float:
        vals = HydrologyMetrics._extract_values(records, "flow_rate")
        return vals[-1] if vals else 0.0
        
    @staticmethod
    def calculate_capacity_usage(water_level: float, max_capacity: float) -> float:
        if max_capacity <= 0:
            return 0.0
        return (water_level / max_capacity) * 100.0

    @staticmethod
    def check_completeness(context: HydrologyContext) -> float:
        total_expected = 10
        actual = len(context.river_observations)
        return min(1.0, actual / total_expected) if total_expected > 0 else 0.0
