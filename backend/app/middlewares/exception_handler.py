"""Global exception handling."""
import traceback
from datetime import datetime, timezone
from typing import Any

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logger import get_logger
from app.core.correlation import get_correlation_id
from app.config.settings import settings
from app.exceptions.base import AppException
from app.exceptions.api import INTERNAL_SERVER_ERROR, VALIDATION_ERROR

logger = get_logger(__name__)


def format_error_response(
    code: str, 
    message: str, 
    path: str, 
    details: list[Any] | None = None
) -> dict[str, Any]:
    """Format standard enterprise error response."""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or [],
            "correlation_id": get_correlation_id(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": path,
        }
    }


def add_exception_handlers(app: FastAPI) -> None:
    """Register all global exception handlers."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        # Expected business exceptions are logged as warnings
        logger.warning(
            f"AppException: {exc.error_code} - {exc.message}",
            extra={"path": request.url.path, "status_code": exc.status_code}
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=format_error_response(
                code=exc.error_code,
                message=exc.message,
                path=request.url.path,
                details=exc.details
            )
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = exc.errors()
        details = []
        for err in errors:
            details.append({
                "loc": err.get("loc"),
                "msg": err.get("msg"),
                "type": err.get("type")
            })
            
        logger.info(f"Validation Error at {request.url.path}")
            
        return JSONResponse(
            status_code=422,
            content=format_error_response(
                code=VALIDATION_ERROR,
                message="Invalid request payload",
                path=request.url.path,
                details=details
            )
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=format_error_response(
                code="HTTP_ERROR",
                message=str(exc.detail),
                path=request.url.path
            )
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.critical(
            f"Unhandled exception: {str(exc)}", 
            exc_info=exc,
            extra={"path": request.url.path}
        )
        
        # Hide sensitive details in production
        is_dev = settings.app.environment.is_development
        message = str(exc) if is_dev else "An unexpected internal server error occurred."
        
        details = []
        if is_dev:
            details.append({"stack_trace": traceback.format_exception(type(exc), exc, exc.__traceback__)})
            
        return JSONResponse(
            status_code=500,
            content=format_error_response(
                code=INTERNAL_SERVER_ERROR,
                message=message,
                path=request.url.path,
                details=details
            )
        )
