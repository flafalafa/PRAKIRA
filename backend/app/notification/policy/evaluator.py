"""Policy Evaluator."""
from typing import List
from app.notification.policy.context import AlertPolicyContext
from app.notification.policy.result import AlertPolicyResult, PolicyDecision
from app.notification.policy.registry import PolicyRegistry
from app.core.logger import get_logger

logger = get_logger(__name__)

class PolicyEvaluator:
    @staticmethod
    async def evaluate(context: AlertPolicyContext) -> AlertPolicyResult:
        logger.debug(f"Evaluating policies for notification: {context.notification_request.notification_id}")
        
        result = AlertPolicyResult(priority=context.notification_request.priority)
        rules = PolicyRegistry.get_all_rules()
        
        for rule in rules:
            try:
                is_triggered, decision, reason = await rule.evaluate(context)
                if is_triggered:
                    result.triggered_policies.append(rule.name)
                    logger.debug(f"Rule triggered: {rule.name} -> {decision}")
                    
                    if decision == PolicyDecision.SUPPRESS or decision == PolicyDecision.DEFER:
                        result.policy_decision = decision
                        result.delivery_decision = False
                        result.suppression_reason = reason
                        result.explanation = f"Notification suppressed by {rule.name}: {reason}"
                        return result # Fast fail/suppress
                        
                    elif decision == PolicyDecision.ESCALATE:
                        result.policy_decision = decision
                        result.escalation_decision = True
                        result.explanation = f"Notification escalated by {rule.name}: {reason}"
            except Exception as e:
                logger.error(f"Policy Rule {rule.name} failed: {str(e)}")
                
        # If no suppressions triggered, default to SEND
        if result.policy_decision != PolicyDecision.ESCALATE:
            result.policy_decision = PolicyDecision.SEND
            result.explanation = "All policies passed. Safe to deliver."
            
        return result
