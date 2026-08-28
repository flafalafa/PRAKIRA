"""Security Exceptions."""
from app.core.exceptions import BaseDomainException

class SecurityException(BaseDomainException):
    pass

class AuthenticationRequired(SecurityException):
    def __init__(self, message="Authentication required"):
        super().__init__(message)

class InvalidCredentials(SecurityException):
    def __init__(self, message="Invalid credentials provided"):
        super().__init__(message)

class InvalidToken(SecurityException):
    def __init__(self, message="Invalid token"):
        super().__init__(message)

class ExpiredToken(SecurityException):
    def __init__(self, message="Token has expired"):
        super().__init__(message)

class InvalidAPIKey(SecurityException):
    def __init__(self, message="Invalid API Key"):
        super().__init__(message)

class InsufficientPermission(SecurityException):
    def __init__(self, message="Insufficient permissions"):
        super().__init__(message)

class ForbiddenResource(SecurityException):
    def __init__(self, message="Forbidden resource"):
        super().__init__(message)

class SecurityConfigurationError(SecurityException):
    pass
