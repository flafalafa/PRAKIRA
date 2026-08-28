"""Middleware for enterprise request logging and correlation ID."""
import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.core.correlation import set_correlation_id
from app.core.request_context import set_request_context, clear_request_context
from app.core.logger import get_logger

logger = get_logger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to inject correlation ID and log incoming requests."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Get or generate correlation ID
        correlation_id = request.headers.get("X-Correlation-ID")
        correlation_id = set_correlation_id(correlation_id)
        
        # Setup Request Context
        request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("User-Agent", "unknown")
        
        set_request_context(
            request_id=request_id,
            client_ip=client_ip,
            user_agent=user_agent,
            method=request.method,
            url=str(request.url),
        )
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            status_code = 500
            # Re-raise to be handled by global exception handler
            raise e
        finally:
            process_time_ms = round((time.time() - start_time) * 1000, 2)
            
            # Update context with response data
            set_request_context(
                response_status=status_code,
                duration_ms=process_time_ms
            )
            
            # Only log API endpoints
            if request.url.path.startswith("/api"):
                logger.info("Request completed")
                
            clear_request_context()
            
        # Attach Correlation ID to response
        response.headers["X-Correlation-ID"] = correlation_id
        return response
