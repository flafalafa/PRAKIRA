"""Orchestrates the sequence of Collector executions."""
import asyncio
from app.core.logger import get_logger
from app.scheduler.dispatcher import JobDispatcher

logger = get_logger(__name__)

class CollectorOrchestrator:
    """
    Coordinates execution of all collectors.
    Order: BMKG -> OpenWeather -> RainViewer -> River
    """
    @staticmethod
    async def run_all_sequential():
        logger.info("Starting sequential collector orchestration.")
        
        sequence = ["BMKG", "OpenWeather", "RainViewer", "River"]
        
        for provider_name in sequence:
            job_id = f"job_collect_{provider_name.lower()}"
            logger.info(f"Orchestrator triggering: {provider_name}")
            await JobDispatcher.dispatch(job_id)
            
        logger.info("Sequential collector orchestration finished.")
        
    @staticmethod
    async def run_all_parallel():
        logger.info("Starting parallel collector orchestration.")
        sequence = ["BMKG", "OpenWeather", "RainViewer", "River"]
        tasks = []
        for provider_name in sequence:
            job_id = f"job_collect_{provider_name.lower()}"
            tasks.append(JobDispatcher.dispatch(job_id))
            
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("Parallel collector orchestration finished.")
