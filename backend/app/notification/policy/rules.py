"""Alert Policy Rules."""
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from datetime import datetime, timezone
from app.notification.policy.context import AlertPolicyContext
from app.notification.policy.result import PolicyDecision

class BasePolicyRule(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    async def evaluate(self, context: AlertPolicyContext) -> Tuple[bool, Optional[PolicyDecision], str]:
        """Returns (is_triggered, decision, reason)"""
        pass

class DuplicateAlertRule(BasePolicyRule):
    name = "DUPLICATE_ALERT_RULE"
    
    async def evaluate(self, context: AlertPolicyContext) -> Tuple[bool, Optional[PolicyDecision], str]:
        if not context.last_notification:
            return False, None, ""
            
        current = context.notification_request
        last = context.last_notification
        
        # If type and severity are the same, it's a duplicate
        if current.notification_type == last.notification_type and current.severity == last.severity:
            return True, PolicyDecision.SUPPRESS, "Duplicate notification detected"
            
        return False, None, ""

class CooldownPolicyRule(BasePolicyRule):
    name = "COOLDOWN_POLICY_RULE"
    
    def __init__(self, cooldown_minutes: int = 15):
        self.cooldown_minutes = cooldown_minutes
        
    async def evaluate(self, context: AlertPolicyContext) -> Tuple[bool, Optional[PolicyDecision], str]:
        # Emergency bypasses cooldown
        if context.notification_request.priority == "EMERGENCY":
            return False, None, ""
            
        if not context.last_notification:
            return False, None, ""
            
        now = datetime.now(timezone.utc)
        time_since_last = (now - context.last_notification.timestamp).total_seconds() / 60.0
        
        if time_since_last < self.cooldown_minutes:
            return True, PolicyDecision.DEFER, f"In cooldown period ({self.cooldown_minutes}m)"
            
        return False, None, ""

class EscalationRule(BasePolicyRule):
    name = "ESCALATION_RULE"
    
    async def evaluate(self, context: AlertPolicyContext) -> Tuple[bool, Optional[PolicyDecision], str]:
        if not context.last_notification:
            return False, None, ""
            
        current = context.notification_request
        last = context.last_notification
        
        severity_ranks = {"VERY_LOW": 1, "LOW": 2, "MEDIUM": 3, "HIGH": 4, "VERY_HIGH": 5, "EXTREME": 6}
        curr_rank = severity_ranks.get(current.severity, 0)
        last_rank = severity_ranks.get(last.severity, 0)
        
        if curr_rank > last_rank:
            return True, PolicyDecision.ESCALATE, f"Severity escalated from {last.severity} to {current.severity}"
            
        return False, None, ""
