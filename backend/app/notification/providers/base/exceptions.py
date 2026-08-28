"""Provider Base Exceptions."""
from app.notification.exceptions import NotificationException

class ProviderException(NotificationException):
    pass

class ProviderUnavailable(ProviderException):
    pass

class AuthenticationFailure(ProviderException):
    pass

class InvalidDeviceToken(ProviderException):
    pass

class PayloadTooLarge(ProviderException):
    pass

class DeliveryFailure(ProviderException):
    pass

class BatchFailure(ProviderException):
    pass

class HealthCheckFailure(ProviderException):
    pass
