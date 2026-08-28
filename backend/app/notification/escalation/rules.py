"""Escalation & Deduplication Rules."""
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from app.notification.escalation.context import EscalationContext
from app.notification.escalation.result import EngineDecision, EscalationLevel

class BaseEngineRule(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    async def evaluate(self, context: EscalationContext) -> Tuple[bool, EngineDecision, EscalationLevel, str]:
        """Returns (is_triggered, decision, level, reason)"""
        pass

class DeduplicationRule(BaseEngineRule):
    name = "DEDUPLICATION_RULE"
    
    async def evaluate(self, context: EscalationContext) -> Tuple[bool, EngineDecision, EscalationLevel, str]:
        last = context.history.get_last_notification()
        if not last:
            return False, EngineDecision.PROCEED, EscalationLevel.NO_CHANGE, ""
            
        curr = context.current_job.request
        prev = last.request
        
        if curr.notification_type == prev.notification_type and curr.severity == prev.severity:
            return True, EngineDecision.SUPPRESS, EscalationLevel.NO_CHANGE, "Semantically equivalent to last notification"
            
        return False, EngineDecision.PROCEED, EscalationLevel.NO_CHANGE, ""

class SeverityUpgradeRule(BaseEngineRule):
    name = "SEVERITY_UPGRADE_RULE"
    
    async def evaluate(self, context: EscalationContext) -> Tuple[bool, EngineDecision, EscalationLevel, str]:
        if context.current_job.priority == "EMERGENCY":
            return True, EngineDecision.PROCEED, EscalationLevel.EMERGENCY_OVERRIDE, "Emergency override active"
            
        last = context.history.get_last_notification()
        if not last:
            return False, EngineDecision.PROCEED, EscalationLevel.NO_CHANGE, ""
            
        severity_ranks = {"SAFE": 1, "WATCH": 2, "WARNING": 3, "DANGER": 4, "EMERGENCY": 5}
        curr_rank = severity_ranks.get(context.current_job.request.severity, 0)
        last_rank = severity_ranks.get(last.request.severity, 0)
        
        if curr_rank > last_rank:
            queued = context.history.get_queued_notifications()
            if queued:
                return True, EngineDecision.REPLACE, EscalationLevel.UPGRADE, "Severity upgraded, replacing queued jobs"
            return True, EngineDecision.PROCEED, EscalationLevel.UPGRADE, "Severity upgraded"
            
        return False, EngineDecision.PROCEED, EscalationLevel.NO_CHANGE, ""
