"""Application lifespan configuration."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events."""
    # Import orchestrator to trigger module-level EngineRegistry.register() calls.
    # This ensures weather, hydrology, and radar engines are registered before
    # any request reaches DecisionWorkflow.execute().
    import app.decision.orchestrator.orchestrator  # noqa: F401
    logger.info("Decision Engines registered via orchestrator bootstrap.")

    logger.info("Application Started")
    
    yield
    
    logger.info("Application Stopped")
