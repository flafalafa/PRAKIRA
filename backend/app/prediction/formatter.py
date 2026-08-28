"""Prediction Formatter."""
from app.decision.risk.result import FloodRiskAssessmentResult

class PredictionFormatter:
    @staticmethod
    def format_recommendation(risk_result: FloodRiskAssessmentResult) -> str:
        recs = risk_result.recommended_actions
        if not recs:
            return "No Action Required"
        # Prioritize the most critical recommendation
        if "Immediate Evacuation Recommended" in recs:
            return "Immediate Evacuation"
        if "Prepare Evacuation" in recs:
            return "Prepare Family"
        if "Prepare Vehicle Relocation" in recs:
            return "Move Valuable Items"
        return "Continue Monitoring"
