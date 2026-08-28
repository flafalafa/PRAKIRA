"""Notification Foundation specific exceptions."""
from app.core.exceptions import AppBaseException

class NotificationException(AppBaseException):
    pass

class NotificationBuildFailure(NotificationException):
    pass

class InvalidPrediction(NotificationException):
    pass

class InvalidPriority(NotificationException):
    pass

class ChannelRegistrationFailure(NotificationException):
    pass

class TemplateFailure(NotificationException):
    pass
