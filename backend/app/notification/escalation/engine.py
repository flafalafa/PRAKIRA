"""Main Escalation & Deduplication Engine."""
from app.notification.escalation.context import EscalationContext
from app.notification.escalation.result import EscalationDecisionResult
from app.notification.escalation.deduplicator import Deduplicator
from app.notification.escalation.escalator import Escalator
from app.notification.escalation.registry import EscalationRuleRegistry
from app.notification.escalation.rules import DeduplicationRule, SeverityUpgradeRule
from app.core.logger import get_logger

logger = get_logger(__name__)

EscalationRuleRegistry.register(DeduplicationRule())
EscalationRuleRegistry.register(SeverityUpgradeRule())

class EscalationEngine:
    @staticmethod
    async def process(context: EscalationContext) -> EscalationDecisionResult:
        job = context.current_job
        logger.info(f"Escalation Engine Started for job: {job.schedule_id}")
        
        result = EscalationDecisionResult(final_priority=job.priority)
        
        # 1. Deduplication (Fast Fail)
        suppressed = await Deduplicator.process(context, result)
        if suppressed:
            logger.info("Engine stopped due to deduplication")
            return result
            
        # 2. Escalation & Replacement
        await Escalator.process(context, result)
        
        if not result.explanation:
            result.explanation = "Engine processed normally. No escalations or duplicates."
            
        logger.info(f"Escalation Engine Completed: {result.decision.value}")
        return result
