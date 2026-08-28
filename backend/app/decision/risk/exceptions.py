"""Risk Assessment specific exceptions."""
from app.decision.exceptions import DecisionEngineException

class RiskAssessmentException(DecisionEngineException):
    pass

class InvalidAssessmentContext(RiskAssessmentException):
    pass

class AggregationFailure(RiskAssessmentException):
    pass

class RiskCalculationFailure(RiskAssessmentException):
    pass

class InvalidWeightConfiguration(RiskAssessmentException):
    pass

class RecommendationFailure(RiskAssessmentException):
    pass
