"""Prediction Generator."""
from app.decision.orchestrator.result import OrchestratorResult
from app.prediction.builder import PredictionBuilder
from app.prediction.classifier import PredictionClassifier
from app.prediction.explainer import PredictionExplainer
from app.prediction.formatter import PredictionFormatter
from app.prediction.validator import PredictionValidator
from app.prediction.result import FloodPredictionResult
from app.prediction.exceptions import InvalidDecisionResult
from app.core.logger import get_logger

logger = get_logger(__name__)

class PredictionGenerator:
    @staticmethod
    def generate(orchestrator_result: OrchestratorResult) -> FloodPredictionResult:
        if not getattr(orchestrator_result, 'risk_result', None):
            raise InvalidDecisionResult("Missing Risk Result in Orchestrator Output")
            
        logger.debug("Building prediction from risk result...")
        
        # 1. Build Base
        prediction = PredictionBuilder.build_initial(orchestrator_result)
        
        # 2. Classify Status
        prediction.prediction_status = PredictionClassifier.classify(orchestrator_result.risk_result)
        
        # 3. Explain
        prediction.explanation = PredictionExplainer.generate_explanation(orchestrator_result.risk_result)
        
        # 4. Format Recommendations
        prediction.recommendation = PredictionFormatter.format_recommendation(orchestrator_result.risk_result)
        
        # 5. Validate
        PredictionValidator.validate(prediction)
        
        return prediction
