"""Main Enterprise Scheduler process."""
import asyncio
from app.core.logger import get_logger
from app.scheduler.orchestrator import CollectorOrchestrator
from app.scheduler.exceptions import SchedulerStopped

logger = get_logger(__name__)

class EnterpriseScheduler:
    def __init__(self, interval_seconds: int = 3600):
        self.interval_seconds = interval_seconds
        self._running = False
        self._task = None
        
    async def start(self):
        if self._running:
            return
        self._running = True
        logger.info("Enterprise Scheduler Started.")
        self._task = asyncio.create_task(self._loop())
        
    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Enterprise Scheduler Stopped.")
        
    async def pause(self):
        self._running = False
        logger.info("Enterprise Scheduler Paused.")
        
    async def resume(self):
        await self.start()
        
    async def manual_trigger(self):
        logger.info("Manual Trigger initiated.")
        await CollectorOrchestrator.run_all_sequential()
        
    async def _loop(self):
        while self._running:
            try:
                logger.info("Scheduler executing tick.")
                await CollectorOrchestrator.run_all_sequential()
            except Exception as e:
                logger.error(f"Scheduler tick failed: {str(e)}")
                
            if self._running:
                await asyncio.sleep(self.interval_seconds)
