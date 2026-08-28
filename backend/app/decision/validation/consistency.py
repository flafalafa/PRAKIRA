"""Consistency Validation."""
from app.prediction.result import FloodPredictionResult
from app.decision.validation.exceptions import ConsistencyFailure

class ConsistencyValidator:
    @staticmethod
    def validate(prediction: FloodPredictionResult) -> bool:
        """Validates internal consistency of the prediction result."""
        # Risk vs Status consistency
        if prediction.risk_score >= 90 and prediction.prediction_status != "EMERGENCY":
            raise ConsistencyFailure(f"Inconsistent risk_score {prediction.risk_score} for status {prediction.prediction_status}")
            
        # Explanation availability
        if not prediction.explanation:
            raise ConsistencyFailure("Prediction explanation is missing")
            
        return True
