"""Deduplicator Module."""
from app.notification.escalation.context import EscalationContext
from app.notification.escalation.result import EscalationDecisionResult, EngineDecision
from app.notification.escalation.rules import DeduplicationRule
from app.core.logger import get_logger

logger = get_logger(__name__)

class Deduplicator:
    @staticmethod
    async def process(context: EscalationContext, result: EscalationDecisionResult) -> bool:
        """Returns True if suppressed."""
        rule = DeduplicationRule()
        is_triggered, decision, level, reason = await rule.evaluate(context)
        
        if is_triggered and decision == EngineDecision.SUPPRESS:
            result.decision = decision
            result.duplicate_status = True
            result.suppression_reason = reason
            result.explanation = f"Deduplication: {reason}"
            result.triggered_policies.append(rule.name)
            logger.info(f"Duplicate detected: {context.current_job.notification_id}")
            return True
            
        return False
