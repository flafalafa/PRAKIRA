"""Prediction Classifier."""
from app.decision.risk.result import FloodRiskAssessmentResult
from app.prediction.result import PredictionStatus

class PredictionClassifier:
    @staticmethod
    def classify(risk_result: FloodRiskAssessmentResult) -> PredictionStatus:
        score = risk_result.risk_score
        if score >= 90:
            return PredictionStatus.EMERGENCY
        elif score >= 75:
            return PredictionStatus.DANGER
        elif score >= 60:
            return PredictionStatus.WARNING
        elif score >= 40:
            return PredictionStatus.WATCH
        return PredictionStatus.SAFE
