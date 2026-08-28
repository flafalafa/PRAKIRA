"""Main Alert Policy Engine."""
from app.notification.policy.context import AlertPolicyContext
from app.notification.policy.result import AlertPolicyResult
from app.notification.policy.evaluator import PolicyEvaluator
from app.notification.policy.registry import PolicyRegistry
from app.notification.policy.rules import DuplicateAlertRule, CooldownPolicyRule, EscalationRule
from app.core.logger import get_logger

logger = get_logger(__name__)

# Auto-register default rules
PolicyRegistry.register(DuplicateAlertRule())
PolicyRegistry.register(CooldownPolicyRule())
PolicyRegistry.register(EscalationRule())

class AlertPolicyEngine:
    @staticmethod
    async def evaluate(context: AlertPolicyContext) -> AlertPolicyResult:
        logger.info(f"Policy Evaluation Started for: {context.notification_request.notification_id}")
        
        try:
            result = await PolicyEvaluator.evaluate(context)
            if not result.delivery_decision:
                logger.info(f"Notification Suppressed: {context.notification_request.notification_id} - {result.suppression_reason}")
            elif result.escalation_decision:
                logger.info(f"Notification Escalated: {context.notification_request.notification_id}")
            else:
                logger.info(f"Notification Passed Policies: {context.notification_request.notification_id}")
                
            return result
        except Exception as e:
            logger.error(f"Policy Evaluation Failed: {str(e)}")
            raise
