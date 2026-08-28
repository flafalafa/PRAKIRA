"""Security Policies."""
from app.api.security.context import SecurityContext
from app.api.security.roles import Role
from app.api.security.permissions import Permission
from app.api.security.exceptions import InsufficientPermission, ForbiddenResource

class SecurityPolicy:
    @staticmethod
    def require_role(context: SecurityContext, role: Role) -> bool:
        if role not in context.roles and Role.ADMIN not in context.roles:
            raise ForbiddenResource(f"Requires role: {role.value}")
        return True
        
    @staticmethod
    def require_permission(context: SecurityContext, permission: Permission) -> bool:
        if permission not in context.permissions and Role.ADMIN not in context.roles:
            raise InsufficientPermission(f"Requires permission: {permission.value}")
        return True
