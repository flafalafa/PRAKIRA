"""Security Roles."""
from enum import Enum

class Role(str, Enum):
    PUBLIC = "PUBLIC"
    USER = "USER"
    OPERATOR = "OPERATOR"
    ADMIN = "ADMIN"
    GOVERNMENT = "GOVERNMENT"
    SERVICE = "SERVICE"
