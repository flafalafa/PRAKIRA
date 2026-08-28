"""Prediction Builder."""
import uuid
from app.decision.orchestrator.result import OrchestratorResult
from app.decision.risk.result import FloodRiskAssessmentResult
from app.prediction.result import FloodPredictionResult

class PredictionBuilder:
    @staticmethod
    def build_initial(orchestrator_result: OrchestratorResult) -> FloodPredictionResult:
        risk_result: FloodRiskAssessmentResult = orchestrator_result.risk_result
        
        eta = None
        if orchestrator_result.radar_result:
            eta = orchestrator_result.radar_result.estimated_arrival_time
            
        return FloodPredictionResult(
            prediction_id=str(uuid.uuid4()),
            prediction_code=f"PRD-{int(orchestrator_result.timestamp.timestamp())}",
            risk_score=risk_result.risk_score,
            risk_level=risk_result.risk_level,
            confidence=risk_result.confidence,
            estimated_arrival_time=eta,
            supporting_factors=risk_result.risk_factors
        )
