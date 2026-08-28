"""Main Hydrology Analysis Engine."""
import uuid
from app.decision.hydrology.context import HydrologyContext
from app.decision.hydrology.result import HydrologyAnalysisResult, HydrologySeverity, RiverStatus
from app.decision.hydrology.analyzer import HydrologyAnalyzer
from app.decision.hydrology.metrics import HydrologyMetrics
from app.decision.hydrology.policy import HydrologyPolicyEngine
from app.decision.explanation import DecisionExplanation, ReasonSummary
from app.core.logger import get_logger

logger = get_logger(__name__)

class HydrologyAnalysisEngine:
    @staticmethod
    async def analyze(context: HydrologyContext) -> HydrologyAnalysisResult:
        logger.info(f"Hydrology Analysis Started: {context.analysis_id}")
        
        # 1. Metrics Calculation
        current_level = HydrologyMetrics.get_latest_water_level(context.river_observations)
        rise_rate = HydrologyMetrics.calculate_rise_rate(context.river_observations)
        flow_rate = HydrologyMetrics.get_latest_flow_rate(context.river_observations)
        max_cap = context.river_metadata.get("max_capacity_cm", 300.0)
        capacity_usage = HydrologyMetrics.calculate_capacity_usage(current_level, max_cap)
        completeness = HydrologyMetrics.check_completeness(context)
        
        # 2. Rule Execution
        triggered_rules = await HydrologyAnalyzer.execute_rules(context)
        
        # Determine status
        river_status = RiverStatus.RISING if rise_rate > 0 else RiverStatus.RECEDING
        if capacity_usage > 100:
            river_status = RiverStatus.OVERFLOW
        elif rise_rate == 0:
            river_status = RiverStatus.NORMAL
        
        # 3. Base Result Creation
        result = HydrologyAnalysisResult(
            analysis_id=context.analysis_id,
            current_water_level=current_level,
            water_level_trend="RISING" if rise_rate > 0 else "FALLING",
            river_capacity_usage=capacity_usage,
            flow_rate=flow_rate,
            flow_trend="STEADY",
            river_status=river_status,
            hydrology_severity=HydrologySeverity.WARNING if capacity_usage > 80 else HydrologySeverity.NORMAL,
            confidence=completeness,
            triggered_rules=triggered_rules,
            explanation=DecisionExplanation()
        )
        
        # 4. Add Explanation reasons
        for rule in triggered_rules:
            result.explanation.reasons.append(
                ReasonSummary(rule_name=rule, description=f"{rule} condition met.", impact=1.0)
            )
            
        # 5. Apply Policies
        result = HydrologyPolicyEngine.apply_policies(result, completeness)
        
        logger.info(f"Hydrology Analysis Completed: {context.analysis_id}")
        return result
