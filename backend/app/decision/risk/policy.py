"""Risk Policy Engine."""
from app.decision.risk.result import FloodRiskAssessmentResult, RiskLevel

class RiskPolicyEngine:
    @staticmethod
    def apply_policies(result: FloodRiskAssessmentResult) -> FloodRiskAssessmentResult:
        score = result.risk_score
        if score >= 90:
            result.risk_level = RiskLevel.EXTREME
        elif score >= 75:
            result.risk_level = RiskLevel.VERY_HIGH
        elif score >= 60:
            result.risk_level = RiskLevel.HIGH
        elif score >= 40:
            result.risk_level = RiskLevel.MEDIUM
        elif score >= 20:
            result.risk_level = RiskLevel.LOW
        else:
            result.risk_level = RiskLevel.VERY_LOW
            
        return result
