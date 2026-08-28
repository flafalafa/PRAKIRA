"""Main Weather Analysis Engine."""
import uuid
from app.decision.weather.context import WeatherContext
from app.decision.weather.result import WeatherAnalysisResult, WeatherSeverity
from app.decision.weather.analyzer import WeatherAnalyzer
from app.decision.weather.metrics import WeatherMetrics
from app.decision.weather.policy import WeatherPolicyEngine
from app.decision.explanation import DecisionExplanation, ReasonSummary
from app.core.logger import get_logger

logger = get_logger(__name__)

class WeatherAnalysisEngine:
    @staticmethod
    async def analyze(context: WeatherContext) -> WeatherAnalysisResult:
        logger.info(f"Weather Analysis Started: {context.analysis_id}")
        
        # 1. Metrics Calculation
        avg_rainfall = WeatherMetrics.calculate_average_rainfall(context.rainfall_observations)
        accumulation = WeatherMetrics.calculate_accumulation(context.rainfall_observations)
        completeness = WeatherMetrics.check_completeness(context)
        
        # 2. Rule Execution
        triggered_rules = await WeatherAnalyzer.execute_rules(context)
        
        # 3. Base Result Creation
        result = WeatherAnalysisResult(
            analysis_id=context.analysis_id,
            rainfall_intensity=avg_rainfall,
            confidence=completeness,
            triggered_rules=triggered_rules,
            rainfall_summary=f"Avg: {avg_rainfall:.2f}mm, Total: {accumulation:.2f}mm",
            storm_indicator="HEAVY_RAIN" in triggered_rules,
            explanation=DecisionExplanation()
        )
        
        # 4. Add Explanation reasons
        for rule in triggered_rules:
            result.explanation.reasons.append(
                ReasonSummary(rule_name=rule, description=f"{rule} detected.", impact=1.0)
            )
            
        # 5. Apply Policies
        result = WeatherPolicyEngine.apply_policies(result, completeness)
        
        logger.info(f"Weather Analysis Completed: {context.analysis_id}")
        return result
