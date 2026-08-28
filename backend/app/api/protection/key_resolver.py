"""Key Resolution Logic."""
from fastapi import Request
from typing import Optional

def resolve_identity_key(request: Request) -> str:
    """
    Resolve the rate limit key based on identity.
    Uses SecurityContext (T-702) if available.
    Falls back to IP address if anonymous.
    Do not blindly trust X-Forwarded-For without proper proxy config.
    """
    # 1. Authenticated Principal
    if hasattr(request.state, "user") and request.state.user:
        # Use principal ID for JWT or API Key identity
        return f"auth:{request.state.user.principal_id}"
        
    # 2. Anonymous IP (fallback)
    # Using request.client.host which is set securely by Uvicorn 
    # based on trusted proxies configuration, preventing spoofing.
    client_ip = request.client.host if request.client else "unknown"
    return f"anon:{client_ip}"
