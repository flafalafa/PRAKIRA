"""Integration and Validation exceptions."""
from app.core.exceptions import AppBaseException

class IntegrationException(AppBaseException):
    pass

class CollectorContractViolation(IntegrationException):
    pass

class PipelineFailure(IntegrationException):
    pass

class CanonicalValidationFailure(IntegrationException):
    pass

class ProviderRegistrationFailure(IntegrationException):
    pass

class ConfigurationError(IntegrationException):
    pass

class IntegrationFailure(IntegrationException):
    pass
