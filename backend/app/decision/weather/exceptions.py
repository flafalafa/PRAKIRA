"""Weather Analysis specific exceptions."""
from app.decision.exceptions import DecisionEngineException

class WeatherAnalysisException(DecisionEngineException):
    pass

class InvalidWeatherData(WeatherAnalysisException):
    pass

class IncompleteDataset(WeatherAnalysisException):
    pass

class MetricCalculationFailure(WeatherAnalysisException):
    pass

class RuleFailure(WeatherAnalysisException):
    pass
