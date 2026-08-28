"""Notification Scheduler specific exceptions."""
from app.notification.exceptions import NotificationException

class SchedulerException(NotificationException):
    pass

class SchedulingFailure(SchedulerException):
    pass

class QueueFailure(SchedulerException):
    pass

class RetryFailure(SchedulerException):
    pass

class TimeoutFailure(SchedulerException):
    pass

class CancellationFailure(SchedulerException):
    pass

class InvalidSchedule(SchedulerException):
    pass
