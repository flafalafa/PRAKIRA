"""Escalation & Deduplication Exceptions."""
from app.notification.exceptions import NotificationException

class EscalationEngineException(NotificationException):
    pass

class DeduplicationFailure(EscalationEngineException):
    pass

class EscalationFailure(EscalationEngineException):
    pass

class ReplacementFailure(EscalationEngineException):
    pass

class PolicyFailure(EscalationEngineException):
    pass

class HistoryFailure(EscalationEngineException):
    pass
