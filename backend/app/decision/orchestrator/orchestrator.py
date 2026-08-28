"""Main Decision Orchestrator."""
from app.decision.orchestrator.context import OrchestratorContext
from app.decision.orchestrator.workflow import DecisionWorkflow
from app.decision.orchestrator.result import OrchestratorResult
from app.decision.weather.engine import WeatherAnalysisEngine
from app.decision.hydrology.engine import HydrologyAnalysisEngine
from app.decision.radar.engine import RadarAnalysisEngine
from app.decision.orchestrator.registry import EngineRegistry

# Auto-register default engines
EngineRegistry.register("weather", WeatherAnalysisEngine, priority=1)
EngineRegistry.register("hydrology", HydrologyAnalysisEngine, priority=2)
EngineRegistry.register("radar", RadarAnalysisEngine, priority=3)

class DecisionOrchestrator:
    @staticmethod
    async def process(context: OrchestratorContext) -> OrchestratorResult:
        """Entry point for the Enterprise Decision Engine."""
        return await DecisionWorkflow.execute(context)
