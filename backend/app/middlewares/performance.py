"""Performance monitoring middleware."""
import time
from fastapi import Request
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response
from app.middlewares.base import PrakiraBaseMiddleware
from app.core.logger import get_logger
from app.config.settings import settings

logger = get_logger(__name__)

class PerformanceMiddleware(PrakiraBaseMiddleware):
    """Middleware to measure request performance and flag slow requests."""
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        
        # Placeholders for future CPU and Memory tracking
        # cpu_time_start = get_cpu_time()
        # memory_usage_start = get_memory_usage()
        
        response = await call_next(request)
        
        duration_ms = (time.time() - start_time) * 1000
        
        if duration_ms > settings.performance.slow_request_threshold_ms:
            logger.warning(
                f"Slow Request Detected: {request.method} {request.url.path} took {duration_ms:.2f}ms",
                extra={
                    "duration_ms": duration_ms,
                    "path": request.url.path,
                    "threshold_ms": settings.performance.slow_request_threshold_ms
                }
            )
            
        return response
