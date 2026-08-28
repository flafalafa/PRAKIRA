"""Endpoint Policies."""
from pydantic import BaseModel
from typing import Dict, List, Optional
import re

class RateLimitPolicy(BaseModel):
    limit: int
    window: int
    description: str

class EndpointPolicyConfig:
    """Centralized policy configuration."""
    
    # Defaults
    DEFAULT_ANONYMOUS = RateLimitPolicy(limit=60, window=60, description="60 req/min anon")
    DEFAULT_AUTHENTICATED = RateLimitPolicy(limit=120, window=60, description="120 req/min auth")
    
    # Specific Endpoint Routes (Regex based on Path)
    POLICIES = {
        r"^/api/v1/areas/[^/]+/flood-status": RateLimitPolicy(limit=300, window=60, description="High burst for flood status"),
        r"^/api/v1/areas/[^/]+/predictions": RateLimitPolicy(limit=30, window=60, description="Expensive prediction history"),
        r"^/api/v1/areas/[^/]+/alerts/active": RateLimitPolicy(limit=500, window=60, description="Emergency Active Alert read"),
    }
    
    @classmethod
    def get_policy(cls, path: str, is_authenticated: bool) -> RateLimitPolicy:
        # Check specific routes
        for pattern, policy in cls.POLICIES.items():
            if re.match(pattern, path):
                return policy
                
        # Fallback to default
        if is_authenticated:
            return cls.DEFAULT_AUTHENTICATED
        return cls.DEFAULT_ANONYMOUS
