"""Maintenance mode middleware."""
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response
from app.middlewares.base import PrakiraBaseMiddleware
from app.config.settings import settings

class MaintenanceModeMiddleware(PrakiraBaseMiddleware):
    """Middleware to intercept requests during maintenance."""
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if settings.features.enable_maintenance_mode:
            # Exclude health checks from maintenance mode
            if not request.url.path.startswith("/api/v1/health"):
                return JSONResponse(
                    status_code=503,
                    content={
                        "success": False,
                        "message": "Service temporarily unavailable."
                    }
                )
        return await call_next(request)
