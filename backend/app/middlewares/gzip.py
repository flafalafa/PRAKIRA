"""GZip middleware configuration."""
from fastapi.middleware.gzip import GZipMiddleware
from typing import Any

def get_gzip_middleware() -> tuple[type, dict[str, Any]]:
    """Returns the GZipMiddleware class and its configuration arguments."""
    return (
        GZipMiddleware, 
        {"minimum_size": 1000}
    )
