"""Prediction Explainer."""
from app.decision.risk.result import FloodRiskAssessmentResult

class PredictionExplainer:
    @staticmethod
    def generate_explanation(risk_result: FloodRiskAssessmentResult) -> str:
        base_reasons = risk_result.explanation.reasons
        if not base_reasons:
            return "Kondisi terpantau aman tanpa ancaman signifikan."
            
        parts = []
        for r in base_reasons:
            parts.append(f"- {r.description}")
            
        return "Berdasarkan analisis sistem:\n" + "\n".join(parts)
