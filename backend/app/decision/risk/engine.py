"""Main Risk Assessment Engine."""
import uuid
from app.decision.risk.context import RiskContext
from app.decision.risk.result import FloodRiskAssessmentResult
from app.decision.risk.calculator import RiskCalculator
from app.decision.risk.metrics import RiskMetrics
from app.decision.risk.policy import RiskPolicyEngine
from app.decision.risk.registry import RiskRuleRegistry
from app.decision.explanation import DecisionExplanation, ReasonSummary
from app.core.logger import get_logger

logger = get_logger(__name__)

class FloodRiskAssessmentEngine:
    @staticmethod
    async def evaluate(context: RiskContext) -> FloodRiskAssessmentResult:
        logger.info(f"Risk Assessment Started: {context.assessment_id}")
        
        # 1. Calculation
        risk_data = RiskCalculator.calculate(context)
        confidence = RiskMetrics.calculate_confidence(context)
        
        # 2. Rule Execution & Recommendations
        triggered_rules = []
        recommendations = ["Continue Monitoring"]
        rules = RiskRuleRegistry.get_all_rules()
        for rule in rules:
            try:
                is_triggered = await rule.evaluate(context, risk_data)
                if is_triggered:
                    triggered_rules.append(rule.name)
                    recommendations.append(rule.get_recommendation())
            except Exception as e:
                logger.error(f"Risk Rule {rule.name} failed: {str(e)}")
                
        # Deduplicate recommendations
        recommendations = list(dict.fromkeys(recommendations))
        
        # 3. Base Result Creation
        result = FloodRiskAssessmentResult(
            assessment_id=context.assessment_id,
            risk_score=risk_data["overall_score"],
            confidence=confidence,
            risk_factors=risk_data["factors"],
            risk_contributions=risk_data["contributions"],
            triggered_rules=triggered_rules,
            recommended_actions=recommendations,
            explanation=DecisionExplanation()
        )
        
        # 4. Add Explanation reasons
        for k, v in risk_data["contributions"].items():
            result.explanation.reasons.append(
                ReasonSummary(rule_name="Contribution", description=f"{k} contributed to risk.", impact=v)
            )
            
        # 5. Apply Policies (Classification)
        result = RiskPolicyEngine.apply_policies(result)
        
        logger.info(f"Risk Assessment Completed: {context.assessment_id}")
        return result
