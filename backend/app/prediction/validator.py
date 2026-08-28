"""Prediction Validator."""
from app.prediction.result import FloodPredictionResult
from app.prediction.exceptions import PredictionValidationFailure
from app.core.logger import get_logger

logger = get_logger(__name__)

class PredictionValidator:
    @staticmethod
    def validate(prediction: FloodPredictionResult) -> bool:
        if not prediction.prediction_id:
            raise PredictionValidationFailure("Prediction ID is missing")
        if prediction.risk_score < 0 or prediction.risk_score > 100:
            raise PredictionValidationFailure("Risk score out of bounds")
        if not prediction.explanation:
            raise PredictionValidationFailure("Explanation is missing")
        logger.debug(f"Prediction {prediction.prediction_id} passed validation.")
        return True
