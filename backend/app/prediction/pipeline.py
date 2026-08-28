"""Main Prediction Generation Pipeline."""
from app.decision.orchestrator.result import OrchestratorResult
from app.prediction.generator import PredictionGenerator
from app.prediction.result import FloodPredictionResult
from app.core.logger import get_logger

logger = get_logger(__name__)

class PredictionPipeline:
    @staticmethod
    def process(orchestrator_result: OrchestratorResult) -> FloodPredictionResult:
        logger.info(f"Prediction Pipeline Started for workflow: {orchestrator_result.workflow_id}")
        try:
            prediction = PredictionGenerator.generate(orchestrator_result)
            logger.info(f"Prediction Completed: {prediction.prediction_id}")
            return prediction
        except Exception as e:
            logger.error(f"Prediction Pipeline Failed: {str(e)}")
            raise
