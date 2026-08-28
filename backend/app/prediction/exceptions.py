"""Prediction Pipeline specific exceptions."""
from app.core.exceptions import AppBaseException

class PredictionException(AppBaseException):
    pass

class PredictionGenerationFailure(PredictionException):
    pass

class PredictionValidationFailure(PredictionException):
    pass

class InvalidDecisionResult(PredictionException):
    pass

class ClassificationFailure(PredictionException):
    pass

class RecommendationFailure(PredictionException):
    pass

class ExplanationFailure(PredictionException):
    pass
