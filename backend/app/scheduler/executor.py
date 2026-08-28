"""Executes a single job with retry and timeout policies."""
import asyncio
from typing import Callable, Any
from app.scheduler.job import Job, JobStatus
from app.scheduler.context import ExecutionContext
from app.scheduler.exceptions import TimeoutError, RetryExceeded, CollectorFailed
from app.core.logger import get_logger

logger = get_logger(__name__)

class JobExecutor:
    @staticmethod
    async def execute(job: Job, func: Callable, *args, **kwargs) -> Any:
        context = ExecutionContext(job.id)
        job.status = JobStatus.RUNNING
        
        for attempt in range(1, job.policy.retry.retry_count + 1):
            context.attempt = attempt
            try:
                logger.debug(f"Executing job {job.id} (Attempt {attempt})")
                
                # Run with timeout
                result = await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=job.policy.timeout.timeout_seconds
                )
                
                context.mark_complete()
                job.status = JobStatus.COMPLETED
                logger.info(f"Job {job.id} completed in {context.duration_seconds:.2f}s")
                return result
                
            except asyncio.TimeoutError:
                logger.warning(f"Job {job.id} timed out on attempt {attempt}")
                if attempt == job.policy.retry.retry_count:
                    job.status = JobStatus.TIMEOUT
                    raise TimeoutError(f"Job {job.id} timed out after {attempt} attempts")
                    
            except Exception as e:
                logger.warning(f"Job {job.id} failed on attempt {attempt}: {str(e)}")
                if attempt == job.policy.retry.retry_count:
                    job.status = JobStatus.FAILED
                    raise CollectorFailed(f"Job {job.id} failed: {str(e)}")
                    
            # Apply backoff
            delay = job.policy.retry.retry_delay_seconds
            if job.policy.retry.exponential_backoff:
                delay *= (2 ** (attempt - 1))
            await asyncio.sleep(delay)
