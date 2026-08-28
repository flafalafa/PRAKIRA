"""Prediction domain exceptions."""
from app.exceptions.base import AppException

class PredictionDomainError(AppException):
    pass

class PredictionValidationError(PredictionDomainError):
    pass

class PredictionStateError(PredictionDomainError):
    pass

class InvalidRiskScore(PredictionValidationError):
    pass

class InvalidProbability(PredictionValidationError):
    pass

class InvalidPredictionConfidence(PredictionValidationError):
    pass

class InvalidForecastWindow(PredictionValidationError):
    pass

class PredictionExpired(PredictionStateError):
    pass

class PredictionCancelled(PredictionStateError):
    pass

class PredictionNotValidated(PredictionStateError):
    pass
