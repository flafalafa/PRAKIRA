"""Workflow Management."""
import time
from app.decision.orchestrator.context import OrchestratorContext
from app.decision.orchestrator.registry import EngineRegistry
from app.decision.orchestrator.pipeline import WorkflowPipeline
from app.decision.orchestrator.result import OrchestratorResult
from app.decision.orchestrator.state import WorkflowState
from app.decision.risk.context import RiskContext
from app.decision.risk.engine import FloodRiskAssessmentEngine
from app.core.logger import get_logger

logger = get_logger(__name__)

class DecisionWorkflow:
    @staticmethod
    async def execute(context: OrchestratorContext) -> OrchestratorResult:
        start_time = time.time()
        result = OrchestratorResult(workflow_id=context.workflow_id, state=WorkflowState.RUNNING)
        logger.info(f"Workflow Started: {context.workflow_id}")
        
        engines = dict(EngineRegistry.get_enabled_engines())
        
        try:
            # 1. Execute Base Engines
            if "weather" in engines:
                try:
                    result.weather_result = await WorkflowPipeline.run_weather(context, engines["weather"]["class"])
                except Exception as e:
                    result.errors.append(f"Weather Engine Failed: {str(e)}")
                    
            if "hydrology" in engines:
                try:
                    result.hydrology_result = await WorkflowPipeline.run_hydrology(context, engines["hydrology"]["class"])
                except Exception as e:
                    result.errors.append(f"Hydrology Engine Failed: {str(e)}")
                    
            if "radar" in engines:
                try:
                    result.radar_result = await WorkflowPipeline.run_radar(context, engines["radar"]["class"])
                except Exception as e:
                    result.errors.append(f"Radar Engine Failed: {str(e)}")
                    
            # 2. Risk Assessment
            risk_ctx = RiskContext(
                assessment_id=context.workflow_id,
                weather_result=result.weather_result,
                hydrology_result=result.hydrology_result,
                radar_result=result.radar_result,
                area_metadata=context.area_metadata,
                historical_metadata=context.historical_metadata
            )
            result.risk_result = await FloodRiskAssessmentEngine.evaluate(risk_ctx)
            
            result.state = WorkflowState.PARTIAL_SUCCESS if result.errors else WorkflowState.SUCCESS
            logger.info(f"Workflow Completed: {context.workflow_id}. State: {result.state}")
            
        except Exception as e:
            result.state = WorkflowState.FAILED
            result.errors.append(f"Workflow Failed: {str(e)}")
            logger.error(f"Workflow Failed: {context.workflow_id}")
            
        result.execution_duration_ms = int((time.time() - start_time) * 1000)
        return result
