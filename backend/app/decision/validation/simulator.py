"""Simulation Runner."""
import time
from app.decision.validation.scenario import ValidationScenario
from app.decision.orchestrator.orchestrator import DecisionOrchestrator
from app.prediction.pipeline import PredictionPipeline
from app.prediction.result import FloodPredictionResult
from app.core.logger import get_logger

logger = get_logger(__name__)

class SimulationRunner:
    @staticmethod
    async def run_scenario(scenario: ValidationScenario) -> FloodPredictionResult:
        start_time = time.time()
        logger.info(f"Simulating scenario: {scenario.name}")
        
        # Run entire pipeline
        orchestrator_result = await DecisionOrchestrator.process(scenario.context)
        prediction = PredictionPipeline.process(orchestrator_result)
        
        duration = int((time.time() - start_time) * 1000)
        logger.debug(f"Simulation completed in {duration}ms")
        
        return prediction
