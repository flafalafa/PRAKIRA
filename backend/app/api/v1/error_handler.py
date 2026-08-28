"""Centralized API Error Handler."""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.exceptions.base import AppException
from app.exceptions.not_found import NotFoundException as NotFoundError
from app.exceptions.authorization import AuthorizationException as ForbiddenError
from app.exceptions.authentication import AuthenticationException as UnauthorizedError
from app.api.v1.schemas.errors import ApiError
from app.api.v1.schemas.error_codes import ErrorCode
import logging
from datetime import datetime, timezone
import traceback

logger = logging.getLogger(__name__)

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        request_id = request.state.request_id if hasattr(request.state, "request_id") else "unknown"
        
        details = {}
        for err in exc.errors():
            loc = "->".join(str(l) for l in err["loc"])
            details[loc] = err["msg"]

        api_error = ApiError(
            error_code=ErrorCode.VALIDATION_ERROR.value,
            message="Request validation failed.",
            details=details,
            request_id=request_id,
            path=request.url.path
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=api_error.model_dump(mode="json")
        )

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        request_id = request.state.request_id if hasattr(request.state, "request_id") else "unknown"
        
        # Map specific domain errors to ErrorCode
        error_code = ErrorCode.INTERNAL_ERROR.value
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        if isinstance(exc, NotFoundError):
            status_code = status.HTTP_404_NOT_FOUND
            # Simple heuristic mapping for domain
            if "Area" in exc.message: error_code = ErrorCode.AREA_NOT_FOUND.value
            elif "Prediction" in exc.message: error_code = ErrorCode.PREDICTION_NOT_FOUND.value
            elif "Alert" in exc.message: error_code = ErrorCode.ALERT_NOT_FOUND.value
            elif "Notification" in exc.message: error_code = ErrorCode.NOTIFICATION_NOT_FOUND.value
            else: error_code = "NOT_FOUND"
        elif isinstance(exc, ForbiddenError):
            status_code = status.HTTP_403_FORBIDDEN
            error_code = ErrorCode.FORBIDDEN.value
        elif isinstance(exc, UnauthorizedError):
            status_code = status.HTTP_401_UNAUTHORIZED
            error_code = ErrorCode.AUTHENTICATION_REQUIRED.value

        api_error = ApiError(
            error_code=error_code,
            message=exc.message,
            request_id=request_id,
            path=request.url.path
        )
        return JSONResponse(
            status_code=status_code,
            content=api_error.model_dump(mode="json")
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        request_id = request.state.request_id if hasattr(request.state, "request_id") else "unknown"
        
        error_code = "HTTP_ERROR"
        if exc.status_code == 401: error_code = ErrorCode.AUTHENTICATION_REQUIRED.value
        elif exc.status_code == 403: error_code = ErrorCode.FORBIDDEN.value
        elif exc.status_code == 404: error_code = "NOT_FOUND"
        elif exc.status_code == 429: error_code = "TOO_MANY_REQUESTS"

        api_error = ApiError(
            error_code=error_code,
            message=str(exc.detail),
            request_id=request_id,
            path=request.url.path
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=api_error.model_dump(mode="json")
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        request_id = request.state.request_id if hasattr(request.state, "request_id") else "unknown"
        
        logger.error(f"Unhandled Exception in request {request_id}: {exc}")
        logger.error(traceback.format_exc())

        api_error = ApiError(
            error_code=ErrorCode.INTERNAL_ERROR.value,
            message="An unexpected server error occurred.",
            request_id=request_id,
            path=request.url.path
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=api_error.model_dump(mode="json")
        )
