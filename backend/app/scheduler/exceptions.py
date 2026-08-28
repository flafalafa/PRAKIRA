"""Scheduler specific exceptions."""
from app.core.exceptions import AppBaseException

class SchedulerException(AppBaseException):
    pass

class JobFailed(SchedulerException):
    pass

class CollectorFailed(SchedulerException):
    pass

class TimeoutError(SchedulerException):
    pass

class RetryExceeded(SchedulerException):
    pass

class SchedulerStopped(SchedulerException):
    pass

class JobCancellationError(SchedulerException):
    pass
