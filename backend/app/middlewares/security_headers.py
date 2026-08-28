"""Security headers middleware."""
from fastapi import Request
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response
from app.middlewares.base import PrakiraBaseMiddleware
from app.config.settings import settings

class SecurityHeadersMiddleware(PrakiraBaseMiddleware):
    """Middleware to inject standard security headers."""
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        sec_settings = settings.security
        response.headers["X-Content-Type-Options"] = sec_settings.content_type_options
        response.headers["X-Frame-Options"] = sec_settings.frame_options
        response.headers["Referrer-Policy"] = sec_settings.referrer_policy
        response.headers["Content-Security-Policy"] = sec_settings.content_security_policy
        response.headers["Permissions-Policy"] = sec_settings.permissions_policy
        response.headers["Strict-Transport-Security"] = sec_settings.strict_transport_security
        return response
