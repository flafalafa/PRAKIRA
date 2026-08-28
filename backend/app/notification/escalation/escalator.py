"""Escalator Module."""
from app.notification.escalation.context import EscalationContext
from app.notification.escalation.result import EscalationDecisionResult, EngineDecision, EscalationLevel
from app.notification.escalation.rules import SeverityUpgradeRule
from app.core.logger import get_logger

logger = get_logger(__name__)

class Escalator:
    @staticmethod
    async def process(context: EscalationContext, result: EscalationDecisionResult) -> None:
        rule = SeverityUpgradeRule()
        is_triggered, decision, level, reason = await rule.evaluate(context)
        
        if is_triggered:
            result.escalation_level = level
            result.triggered_policies.append(rule.name)
            
            if decision == EngineDecision.REPLACE:
                result.decision = decision
                result.replacement_status = True
                result.explanation = f"Escalation requires replacement: {reason}"
                logger.info(f"Notification Replacement triggered: {context.current_job.notification_id}")
            elif level == EscalationLevel.EMERGENCY_OVERRIDE:
                result.explanation = f"Emergency override: {reason}"
                logger.info(f"Emergency Override triggered: {context.current_job.notification_id}")
            else:
                result.explanation = f"Escalation detected: {reason}"
                logger.info(f"Escalation detected: {context.current_job.notification_id}")
