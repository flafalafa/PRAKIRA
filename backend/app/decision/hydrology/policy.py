"""Hydrology Analysis Policy Engine."""
from app.decision.hydrology.result import HydrologyAnalysisResult, HydrologySeverity
from app.decision.explanation import ReasonSummary

class HydrologyPolicyEngine:
    @staticmethod
    def apply_policies(result: HydrologyAnalysisResult, completeness: float) -> HydrologyAnalysisResult:
        if completeness < 0.5:
            result.confidence = min(result.confidence, 0.4)
            result.explanation.reasons.append(
                ReasonSummary(
                    rule_name="Low Completeness Policy",
                    description="Missing river observations detected, capping confidence.",
                    impact=-0.6
                )
            )
            
        if result.river_capacity_usage > 100.0:
            result.hydrology_severity = HydrologySeverity.CRITICAL
            result.explanation.reasons.append(
                ReasonSummary(
                    rule_name="Overflow Policy",
                    description="River capacity exceeded 100%.",
                    impact=1.0
                )
            )
            
        return result
