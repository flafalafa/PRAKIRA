"""Weather Metrics Calculator."""
from typing import List
from app.decision.weather.context import WeatherContext
from app.pipeline.canonical import CanonicalRecord

class WeatherMetrics:
    @staticmethod
    def calculate_average_rainfall(records: List[CanonicalRecord]) -> float:
        vals = []
        for r in records:
            for m in r.measurements:
                if m.parameter.lower() in ("rainfall", "precipitation", "rain"):
                    vals.append(m.value)
        if not vals:
            return 0.0
        return sum(vals) / len(vals)

    @staticmethod
    def calculate_accumulation(records: List[CanonicalRecord]) -> float:
        vals = []
        for r in records:
            for m in r.measurements:
                if m.parameter.lower() in ("rainfall", "precipitation", "rain"):
                    vals.append(m.value)
        return sum(vals)

    @staticmethod
    def check_completeness(context: WeatherContext) -> float:
        total_expected = 10
        actual = len(context.weather_observations) + len(context.rainfall_observations)
        return min(1.0, actual / total_expected) if total_expected > 0 else 0.0
