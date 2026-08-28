"""Dependencies Init."""
from fastapi import Request
from typing import Dict, Any

async def get_request_metadata(request: Request) -> Dict[str, Any]:
    return {
        "request_id": request.state.request_id if hasattr(request.state, "request_id") else "unknown",
        "correlation_id": request.state.correlation_id if hasattr(request.state, "correlation_id") else "unknown",
        "path": request.url.path,
        "method": request.method
    }
