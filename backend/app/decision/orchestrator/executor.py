"""Engine Executor."""
from typing import Any
from app.core.logger import get_logger

logger = get_logger(__name__)

class EngineExecutor:
    @staticmethod
    async def execute(engine_name: str, engine_class: Any, context: Any) -> Any:
        try:
            logger.debug(f"Executing engine: {engine_name}")
            result = await engine_class.analyze(context) if hasattr(engine_class, "analyze") else await engine_class.evaluate(context)
            return result
        except Exception as e:
            logger.error(f"Engine execution failed for {engine_name}: {str(e)}")
            raise
