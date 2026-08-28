"""Alert Policy specific exceptions."""
from app.notification.exceptions import NotificationException

class AlertPolicyException(NotificationException):
    pass

class PolicyEvaluationFailure(AlertPolicyException):
    pass

class InvalidNotification(AlertPolicyException):
    pass

class InvalidPolicyConfiguration(AlertPolicyException):
    pass

class RuleFailure(AlertPolicyException):
    pass

class CooldownFailure(AlertPolicyException):
    pass

class EscalationFailure(AlertPolicyException):
    pass
