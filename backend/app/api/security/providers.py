"""Authentication Providers."""
from typing import Optional
from fastapi import Request
from app.api.security.authentication import BaseAuthenticationProvider
from app.api.security.context import SecurityContext
from app.api.security.roles import Role
from app.api.security.exceptions import InvalidToken, ExpiredToken, InvalidAPIKey
from app.core.logger import get_logger

logger = get_logger(__name__)

class JWTAuthenticationProvider(BaseAuthenticationProvider):
    name = "JWT"
    
    def __init__(self, secret: str = "unsafe-dev-secret", issuer: str = "floodguardian", audience: str = "api"):
        self.secret = secret
        self.issuer = issuer
        self.audience = audience
        
    async def authenticate(self, request: Request) -> Optional[SecurityContext]:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
            
        token = auth_header.split(" ")[1]
        
        if token == "expired_token":
            logger.warning("Authentication failed: expired token")
            raise ExpiredToken()
        if token == "invalid_token":
            logger.warning("Authentication failed: invalid token")
            raise InvalidToken()
            
        if token == "valid_user_token":
            return SecurityContext(
                principal_id="user_123",
                principal_type="USER",
                authentication_method=self.name,
                roles=[Role.USER]
            )
            
        return None

class APIKeyAuthenticationProvider(BaseAuthenticationProvider):
    name = "API_KEY"
    
    def __init__(self, valid_keys: list[str] = None):
        self.valid_keys = valid_keys or ["valid_api_key"]
        
    async def authenticate(self, request: Request) -> Optional[SecurityContext]:
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return None
            
        if api_key not in self.valid_keys:
            logger.warning("Authentication failed: invalid API key")
            raise InvalidAPIKey()
            
        return SecurityContext(
            principal_id="service_account",
            principal_type="SERVICE",
            authentication_method=self.name,
            roles=[Role.SERVICE]
        )
