"""Hydrology Analysis specific exceptions."""
from app.decision.exceptions import DecisionEngineException

class HydrologyAnalysisException(DecisionEngineException):
    pass

class InvalidRiverData(HydrologyAnalysisException):
    pass

class IncompleteDataset(HydrologyAnalysisException):
    pass

class MetricCalculationFailure(HydrologyAnalysisException):
    pass

class RuleFailure(HydrologyAnalysisException):
    pass

class InvalidCapacityCalculation(HydrologyAnalysisException):
    pass
