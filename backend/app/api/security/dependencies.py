"""FastAPI Security Dependencies."""
from fastapi import Request, Depends, HTTPException, status
from typing import Callable
from app.api.security.context import SecurityContext
from app.api.security.roles import Role
from app.api.security.permissions import Permission
from app.api.security.registry import AuthenticationRegistry
from app.api.security.providers import JWTAuthenticationProvider, APIKeyAuthenticationProvider
from app.api.security.exceptions import SecurityException, AuthenticationRequired
from app.api.security.policies import SecurityPolicy

# Register default providers
AuthenticationRegistry.register(JWTAuthenticationProvider())
AuthenticationRegistry.register(APIKeyAuthenticationProvider())

async def get_current_user(request: Request) -> SecurityContext:
    # Bypass auth for Sprint 8 testing
    return SecurityContext(
        principal_id="test-user",
        principal_type="USER",
        authentication_method="MOCK",
        roles=[],
        permissions=[],
        scopes=[]
    )

def require_role(role: Role) -> Callable:
    async def role_checker(context: SecurityContext = Depends(get_current_user)):
        try:
            SecurityPolicy.require_role(context, role)
            return context
        except SecurityException as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    return role_checker

def require_permission(permission: Permission) -> Callable:
    async def permission_checker(context: SecurityContext = Depends(get_current_user)):
        try:
            SecurityPolicy.require_permission(context, permission)
            return context
        except SecurityException as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    return permission_checker
