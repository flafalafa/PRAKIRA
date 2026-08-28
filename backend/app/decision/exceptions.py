"""Decision Engine specific exceptions."""
from app.core.exceptions import AppBaseException

class DecisionEngineException(AppBaseException):
    pass

class InvalidDecisionContext(DecisionEngineException):
    pass

class MissingObservation(DecisionEngineException):
    pass

class RuleExecutionFailure(DecisionEngineException):
    pass

class PolicyFailure(DecisionEngineException):
    pass

class DecisionAggregationFailure(DecisionEngineException):
    pass
