"""Radar Motion Analysis specific exceptions."""
from app.decision.exceptions import DecisionEngineException

class RadarAnalysisException(DecisionEngineException):
    pass

class InvalidRadarFrames(RadarAnalysisException):
    pass

class InsufficientFrames(RadarAnalysisException):
    pass

class MotionCalculationFailure(RadarAnalysisException):
    pass

class TrackingFailure(RadarAnalysisException):
    pass

class InvalidTrajectory(RadarAnalysisException):
    pass

class ETAFailure(RadarAnalysisException):
    pass
