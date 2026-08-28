"""Weather Analysis Policy Engine."""
from app.decision.weather.result import WeatherAnalysisResult, WeatherSeverity
from app.decision.explanation import ReasonSummary

class WeatherPolicyEngine:
    @staticmethod
    def apply_policies(result: WeatherAnalysisResult, completeness: float) -> WeatherAnalysisResult:
        if completeness < 0.5:
            result.confidence = min(result.confidence, 0.4)
            result.explanation.reasons.append(
                ReasonSummary(
                    rule_name="Low Completeness Policy",
                    description="Missing observations detected, capping confidence.",
                    impact=-0.6
                )
            )
            
        if result.rainfall_intensity > 20.0:
            result.weather_severity = WeatherSeverity.SEVERE
            
        return result
