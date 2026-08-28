"""Rule Registry."""
from typing import Dict, List
from app.notification.escalation.rules import BaseEngineRule
from app.core.logger import get_logger

logger = get_logger(__name__)

class EscalationRuleRegistry:
    _rules: Dict[str, BaseEngineRule] = {}
    
    @classmethod
    def register(cls, rule: BaseEngineRule) -> None:
        cls._rules[rule.name] = rule
        
    @classmethod
    def get_all(cls) -> List[BaseEngineRule]:
        return list(cls._rules.values())
