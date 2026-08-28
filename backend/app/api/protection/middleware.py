"""Rate Limiter Middleware."""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.api.protection.limiter import InMemoryTokenBucketLimiter
from app.api.protection.key_resolver import resolve_identity_key
from app.api.protection.policy import EndpointPolicyConfig
from app.api.v1.schemas.errors import ApiError
from app.api.v1.schemas.error_codes import ErrorCode
from app.core.logger import get_logger
import traceback

logger = get_logger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, fail_open: bool = True):
        super().__init__(app)
        self.strategy = InMemoryTokenBucketLimiter()
        self.fail_open = fail_open
        
    async def dispatch(self, request: Request, call_next):
        request_id = request.state.request_id if hasattr(request.state, "request_id") else "unknown"
        path = request.url.path
        
        try:
            # 1. Protection: Reject absurdly large payloads if reading from stream
            if "content-length" in request.headers:
                length = int(request.headers["content-length"])
                if length > 5 * 1024 * 1024: # 5MB limit
                    return self._error_response(
                        ErrorCode.REQUEST_TOO_LARGE.value,
                        "Request body too large.",
                        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        request_id, path
                    )
                    
            # 2. Key Resolution
            identity_key = resolve_identity_key(request)
            is_auth = "auth:" in identity_key
            
            # 3. Policy Application
            policy = EndpointPolicyConfig.get_policy(path, is_auth)
            
            # Full key: includes path to isolate limits per endpoint (or just global per user)
            # For this MVP, we do per user per endpoint policy
            full_key = f"{identity_key}:{path}"
            
            # 4. Check Limit
            is_allowed, remaining, retry_after = await self.strategy.is_allowed(
                full_key, policy.limit, policy.window
            )
            
            if not is_allowed:
                logger.warning(f"Rate limit exceeded for {identity_key} on {path}. Retry after {retry_after}s.")
                resp = self._error_response(
                    ErrorCode.RATE_LIMIT_EXCEEDED.value,
                    "Too many requests.",
                    status.HTTP_429_TOO_MANY_REQUESTS,
                    request_id, path
                )
                resp.headers["Retry-After"] = str(retry_after)
                resp.headers["X-RateLimit-Limit"] = str(policy.limit)
                resp.headers["X-RateLimit-Remaining"] = "0"
                return resp
                
            # Allow Request
            response = await call_next(request)
            
            # Inject successful headers
            response.headers["X-RateLimit-Limit"] = str(policy.limit)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            return response
            
        except Exception as e:
            logger.error(f"Rate Limiter Failure: {e}")
            logger.error(traceback.format_exc())
            if self.fail_open:
                # Bypass limiter on internal failure
                return await call_next(request)
            else:
                return self._error_response(
                    ErrorCode.RATE_LIMITER_UNAVAILABLE.value,
                    "Service protection layer unavailable.",
                    status.HTTP_503_SERVICE_UNAVAILABLE,
                    request_id, path
                )

    def _error_response(self, code: str, msg: str, status_code: int, req_id: str, path: str) -> JSONResponse:
        error = ApiError(
            error_code=code,
            message=msg,
            request_id=req_id,
            path=path
        )
        return JSONResponse(status_code=status_code, content=error.model_dump())
