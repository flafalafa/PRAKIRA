"""Risk Metrics."""
from app.decision.risk.context import RiskContext

class RiskMetrics:
    @staticmethod
    def calculate_confidence(context: RiskContext) -> float:
        confs = []
        if context.weather_result: confs.append(context.weather_result.confidence)
        if context.hydrology_result: confs.append(context.hydrology_result.confidence)
        if context.radar_result: confs.append(context.radar_result.confidence)
        
        if not confs:
            return 0.0
        return sum(confs) / len(confs)
