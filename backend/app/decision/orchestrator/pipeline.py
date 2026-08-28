"""Workflow Pipeline."""
from typing import Any
from app.decision.orchestrator.context import OrchestratorContext
from app.decision.orchestrator.executor import EngineExecutor
from app.decision.weather.context import WeatherContext
from app.decision.hydrology.context import HydrologyContext
from app.decision.radar.context import RadarContext

class WorkflowPipeline:
    @staticmethod
    async def run_weather(context: OrchestratorContext, engine_class: Any) -> Any:
        ctx = WeatherContext(
            analysis_id=context.workflow_id,
            weather_observations=context.weather_observations,
            rainfall_observations=context.rainfall_observations,
            metadata=context.area_metadata
        )
        return await EngineExecutor.execute("weather", engine_class, ctx)

    @staticmethod
    async def run_hydrology(context: OrchestratorContext, engine_class: Any) -> Any:
        ctx = HydrologyContext(
            analysis_id=context.workflow_id,
            river_observations=context.river_observations,
            area_metadata=context.area_metadata,
            river_metadata=context.area_metadata.get("river_metadata", {})
        )
        return await EngineExecutor.execute("hydrology", engine_class, ctx)
        
    @staticmethod
    async def run_radar(context: OrchestratorContext, engine_class: Any) -> Any:
        ctx = RadarContext(
            analysis_id=context.workflow_id,
            radar_observations=context.radar_observations,
            area_metadata=context.area_metadata
        )
        return await EngineExecutor.execute("radar", engine_class, ctx)
