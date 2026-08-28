"""Rule Registry."""
from typing import Dict, List, Type
from app.decision.rules import BaseRule
from app.core.logger import get_logger

logger = get_logger(__name__)

class RuleRegistry:
    _rules: Dict[str, BaseRule] = {}
    
    @classmethod
    def register(cls, rule_instance: BaseRule) -> None:
        cls._rules[rule_instance.name] = rule_instance
        logger.debug(f"Registered rule: {rule_instance.name}")
        
    @classmethod
    def get_all_rules(cls) -> List[BaseRule]:
        return list(cls._rules.values())
