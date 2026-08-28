"""Radar Analysis Policy Engine."""
from app.decision.radar.result import RadarAnalysisResult, RadarSeverity
from app.decision.explanation import ReasonSummary

class RadarPolicyEngine:
    @staticmethod
    def apply_policies(result: RadarAnalysisResult, completeness: float) -> RadarAnalysisResult:
        if completeness < 1.0:
            result.confidence = min(result.confidence, 0.5)
            result.explanation.reasons.append(
                ReasonSummary(
                    rule_name="Insufficient Frames Policy",
                    description="Not enough radar frames for high confidence tracking.",
                    impact=-0.5
                )
            )
            
        if result.estimated_arrival_time is not None and result.estimated_arrival_time <= 30:
            result.radar_severity = RadarSeverity.SEVERE
            result.explanation.reasons.append(
                ReasonSummary(
                    rule_name="Imminent Arrival Policy",
                    description="Storm cell ETA is 30 minutes or less.",
                    impact=1.0
                )
            )
            
        return result
