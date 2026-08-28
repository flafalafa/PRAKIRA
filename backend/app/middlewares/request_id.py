"""Request ID middleware."""
import uuid
from fastapi import Request
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response
from app.middlewares.base import PrakiraBaseMiddleware

class RequestIDMiddleware(PrakiraBaseMiddleware):
    """Middleware to ensure every request has a unique ID."""
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Attach to request state for downstream middlewares
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
