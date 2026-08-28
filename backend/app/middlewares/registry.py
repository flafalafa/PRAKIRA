"""Middleware Registry."""
from fastapi import FastAPI

from app.middlewares.maintenance import MaintenanceModeMiddleware
from app.middlewares.performance import PerformanceMiddleware
from app.middlewares.gzip import get_gzip_middleware
from app.middlewares.cors import get_cors_middleware
from app.middlewares.security_headers import SecurityHeadersMiddleware
from app.middlewares.trusted_host import get_trusted_host_middleware
from app.middlewares.request_logging import RequestLoggingMiddleware
from app.middlewares.request_id import RequestIDMiddleware

def register_middlewares(app: FastAPI) -> None:
    """Register all middlewares in the correct execution order."""
    
    # Fastapi/Starlette executes the LAST added middleware FIRST.
    # Therefore, we add them from INNERMOST (executes last) to OUTERMOST (executes first).
    
    # 9. Maintenance Mode (Innermost, executes right before routing)
    app.add_middleware(MaintenanceModeMiddleware)
    
    # 8. Performance Metrics
    app.add_middleware(PerformanceMiddleware)
    
    # 7. GZip Compression
    gzip_cls, gzip_opts = get_gzip_middleware()
    app.add_middleware(gzip_cls, **gzip_opts)
    
    # 6. CORS (Cross-Origin Resource Sharing)
    cors_cls, cors_opts = get_cors_middleware()
    app.add_middleware(cors_cls, **cors_opts)
    
    # 5. Security Headers
    app.add_middleware(SecurityHeadersMiddleware)
    
    # 4. Trusted Host
    th_cls, th_opts = get_trusted_host_middleware()
    app.add_middleware(th_cls, **th_opts)
    
    # 3. Request Logging (Includes Request Context & Correlation ID handling)
    app.add_middleware(RequestLoggingMiddleware)
    
    # 1. Request ID (Outermost, executes first to assign ID)
    app.add_middleware(RequestIDMiddleware)
