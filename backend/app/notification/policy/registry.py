"""Policy Rule Registry."""
from typing import Dict, List
from app.notification.policy.rules import BasePolicyRule
from app.core.logger import get_logger

logger = get_logger(__name__)

class PolicyRegistry:
    _rules: Dict[str, BasePolicyRule] = {}
    
    @classmethod
    def register(cls, rule_instance: BasePolicyRule) -> None:
        cls._rules[rule_instance.name] = rule_instance
        logger.debug(f"Registered policy rule: {rule_instance.name}")
        
    @classmethod
    def get_all_rules(cls) -> List[BasePolicyRule]:
        return list(cls._rules.values())
