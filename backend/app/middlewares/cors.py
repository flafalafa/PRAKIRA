"""CORS middleware configuration."""
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
from app.config.settings import settings

def get_cors_middleware() -> tuple[type, dict[str, Any]]:
    """Returns the CORSMiddleware class and its configuration arguments."""
    return (
        CORSMiddleware,
        {
            "allow_origins": settings.security.cors_origins,
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }
    )
