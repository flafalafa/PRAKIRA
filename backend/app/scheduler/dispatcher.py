"""Dispatches registered jobs based on triggers or schedules."""
import asyncio
from app.scheduler.registry import JobRegistry
from app.scheduler.executor import JobExecutor
from app.scheduler.job import JobStatus
from app.core.logger import get_logger
from typing import Callable, Dict

logger = get_logger(__name__)

class JobDispatcher:
    _functions: Dict[str, Callable] = {}
    
    @classmethod
    def register_function(cls, target_name: str, func: Callable):
        cls._functions[target_name] = func
        
    @classmethod
    async def dispatch(cls, job_id: str, *args, **kwargs):
        job = JobRegistry.get(job_id)
        if not job:
            logger.error(f"Cannot dispatch: Job {job_id} not found in registry.")
            return
            
        if not job.enabled:
            logger.info(f"Job {job_id} is disabled. Skipping.")
            return
            
        func = cls._functions.get(job.target_func)
        if not func:
            logger.error(f"Target function {job.target_func} not registered for job {job_id}")
            job.status = JobStatus.FAILED
            return
            
        try:
            logger.info(f"Dispatcher triggering job: {job_id}")
            await JobExecutor.execute(job, func, *args, **kwargs)
        except Exception as e:
            logger.error(f"Dispatcher caught error for {job_id}: {str(e)}")
