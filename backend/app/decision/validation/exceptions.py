"""Validation specific exceptions."""
from app.core.exceptions import AppBaseException

class ValidationException(AppBaseException):
    pass

class ScenarioFailure(ValidationException):
    pass

class ConsistencyFailure(ValidationException):
    pass

class ValidationFailure(ValidationException):
    pass

class SimulationFailure(ValidationException):
    pass

class ReportingFailure(ValidationException):
    pass
