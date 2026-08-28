"""Application factory module."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.config.settings import settings
from app.config.constants import PROJECT_NAME, PROJECT_DESCRIPTION, PROJECT_VERSION, CONTACT_NAME, CONTACT_EMAIL, LICENSE_NAME
from app.lifespan import lifespan
from app.api.router import api_router
from app.middlewares.exception_handler import add_exception_handlers
from app.middlewares.registry import register_middlewares
from app.core.logging_config import setup_enterprise_logging
from app.core.bootstrap import bootstrap_di
from app.health.services import register_health_checks


def create_app() -> FastAPI:
    """Application factory for creating FastAPI instance."""
    
    # Initialize structured logging before creating app
    setup_enterprise_logging()
    
    # Bootstrap Dependency Injection Container
    bootstrap_di()
    
    # Register Health Check services
    register_health_checks()

    app = FastAPI(
        title=PROJECT_NAME,
        description=PROJECT_DESCRIPTION,
        version=PROJECT_VERSION,
        contact={"name": CONTACT_NAME, "email": CONTACT_EMAIL},
        license_info={"name": LICENSE_NAME},
        openapi_url=f"{settings.api.prefix}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
        debug=settings.app.debug
    )

    # Register Middlewares via Central Registry
    register_middlewares(app)

    # Register Exception Handlers
    add_exception_handlers(app)

    # Register Routers
    app.include_router(api_router, prefix=settings.api.prefix)

    return app
