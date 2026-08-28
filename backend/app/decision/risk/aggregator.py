"""Risk Aggregator."""
from app.decision.risk.context import RiskContext
from typing import Dict, Any

class RiskAggregator:
    @staticmethod
    def aggregate_factors(context: RiskContext) -> Dict[str, Any]:
        """Aggregates all sub-engine results into a unified factor map."""
        factors = {
            "weather_severity": getattr(context.weather_result, "weather_severity", "NORMAL") if context.weather_result else None,
            "rainfall_intensity": getattr(context.weather_result, "rainfall_intensity", None) if context.weather_result else None,
            "river_capacity_usage": getattr(context.hydrology_result, "river_capacity_usage", None) if context.hydrology_result else None,
            "river_status": getattr(context.hydrology_result, "river_status", "NORMAL") if context.hydrology_result else None,
            "storm_eta": getattr(context.radar_result, "estimated_arrival_time", None) if context.radar_result else None,
            "radar_severity": getattr(context.radar_result, "radar_severity", "NORMAL") if context.radar_result else "NORMAL",
            "radar_confidence": getattr(context.radar_result, "confidence", 0.0) if context.radar_result else 0.0,
            "historical_susceptibility": context.historical_metadata.get("susceptibility_score", 0.0)
        }
        return factors
