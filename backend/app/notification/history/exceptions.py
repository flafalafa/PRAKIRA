"""Notification Tracking Exceptions."""
from app.notification.exceptions import NotificationException

class TrackingException(NotificationException):
    pass

class HistoryCreationFailure(TrackingException):
    pass

class StatusUpdateFailure(TrackingException):
    pass

class TimelineFailure(TrackingException):
    pass

class AuditFailure(TrackingException):
    pass

class QueryFailure(TrackingException):
    pass

class MetricsFailure(TrackingException):
    pass
