"""Core Validator."""
from app.decision.validation.scenario import ValidationScenario
from app.prediction.result import FloodPredictionResult
from app.decision.validation.consistency import ConsistencyValidator
from app.decision.validation.exceptions import ValidationFailure
from app.core.logger import get_logger

logger = get_logger(__name__)

class ScenarioValidator:
    @staticmethod
    def validate_scenario(scenario: ValidationScenario, prediction: FloodPredictionResult) -> bool:
        logger.debug(f"Validating scenario: {scenario.name}")
        
        # 1. Status Check
        if prediction.prediction_status != scenario.expected_status:
            raise ValidationFailure(f"Status mismatch. Expected: {scenario.expected_status}, Got: {prediction.prediction_status}")
            
        # 2. Consistency Check
        ConsistencyValidator.validate(prediction)
        
        return True
