"""Orchestrator specific exceptions."""
from app.decision.exceptions import DecisionEngineException

class OrchestratorException(DecisionEngineException):
    pass

class WorkflowFailure(OrchestratorException):
    pass

class EngineExecutionFailure(OrchestratorException):
    pass

class AggregationFailure(OrchestratorException):
    pass

class ContextFailure(OrchestratorException):
    pass

class TimeoutException(OrchestratorException):
    pass

class CancellationException(OrchestratorException):
    pass
