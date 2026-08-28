"""Security Permissions."""
from enum import Enum

class Permission(str, Enum):
    AREA_READ = "area:read"
    PREDICTION_READ = "prediction:read"
    NOTIFICATION_READ = "notification:read"
    NOTIFICATION_MANAGE = "notification:manage"
    SYSTEM_READ = "system:read"
    SYSTEM_MANAGE = "system:manage"
    ADMIN_MANAGE = "admin:manage"
