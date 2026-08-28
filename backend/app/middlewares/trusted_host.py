"""Trusted Host middleware configuration."""
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from typing import Any
from app.config.settings import settings

def get_trusted_host_middleware() -> tuple[type, dict[str, Any]]:
    """Returns the TrustedHostMiddleware class and its configuration arguments."""
    return (
        TrustedHostMiddleware,
        {"allowed_hosts": settings.security.allowed_hosts}
    )
