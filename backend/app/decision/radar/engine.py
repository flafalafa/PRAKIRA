"""Main Radar Motion Analysis Engine."""
import uuid
from app.decision.radar.context import RadarContext
from app.decision.radar.result import RadarAnalysisResult, RadarSeverity
from app.decision.radar.analyzer import RadarAnalyzer
from app.decision.radar.metrics import RadarMetrics
from app.decision.radar.policy import RadarPolicyEngine
from app.decision.radar.motion import MotionCalculator
from app.decision.radar.tracker import CellTracker
from app.decision.radar.trajectory import TrajectoryEstimator
from app.decision.radar.eta import ETACalculator
from app.decision.explanation import DecisionExplanation, ReasonSummary
from app.core.logger import get_logger

logger = get_logger(__name__)

class RadarAnalysisEngine:
    @staticmethod
    async def analyze(context: RadarContext) -> RadarAnalysisResult:
        logger.info(f"Radar Analysis Started: {context.analysis_id}")
        
        # 0. Completeness Check
        completeness = RadarMetrics.check_completeness(context)
        
        # 1. Pipeline Analysis
        motion_data = MotionCalculator.calculate_vectors(context.radar_observations)
        tracking_data = CellTracker.identify_and_track(context.radar_observations)
        trajectory_data = TrajectoryEstimator.estimate(motion_data, tracking_data)
        eta = ETACalculator.calculate_eta(trajectory_data, motion_data)
        
        analysis_data = {
            "motion": motion_data,
            "tracking": tracking_data,
            "trajectory": trajectory_data,
            "eta": eta
        }
        
        # 2. Metrics
        coverage = RadarMetrics.calculate_coverage(context)
        
        # 3. Rule Execution
        triggered_rules = await RadarAnalyzer.execute_rules(context, analysis_data)
        
        # 4. Base Result Creation
        severity = RadarSeverity.WARNING if eta is not None and eta <= 60 else RadarSeverity.NORMAL
        
        result = RadarAnalysisResult(
            analysis_id=context.analysis_id,
            storm_cells=tracking_data.get("active_cells", 0),
            movement_direction=motion_data.get("avg_direction", 0.0),
            movement_speed=motion_data.get("avg_speed", 0.0),
            estimated_arrival_time=eta,
            coverage_area=coverage,
            radar_severity=severity,
            confidence=completeness,
            triggered_rules=triggered_rules,
            explanation=DecisionExplanation()
        )
        
        # 5. Add Explanation reasons
        for rule in triggered_rules:
            result.explanation.reasons.append(
                ReasonSummary(rule_name=rule, description=f"{rule} condition met.", impact=1.0)
            )
            
        if eta is not None:
            result.explanation.reasons.append(
                ReasonSummary(rule_name="ETA Calculated", description=f"Estimated arrival in {eta} minutes.", impact=0.8)
            )
            
        # 6. Apply Policies
        result = RadarPolicyEngine.apply_policies(result, completeness)
        
        logger.info(f"Radar Analysis Completed: {context.analysis_id}")
        return result
