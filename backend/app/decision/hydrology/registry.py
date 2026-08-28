"""Hydrology Rule Registry."""
from typing import Dict, List
from app.decision.hydrology.rules import BaseHydrologyRule
from app.core.logger import get_logger

logger = get_logger(__name__)

class HydrologyRuleRegistry:
    _rules: Dict[str, BaseHydrologyRule] = {}
    
    @classmethod
    def register(cls, rule_instance: BaseHydrologyRule) -> None:
        cls._rules[rule_instance.name] = rule_instance
        logger.debug(f"Registered hydrology rule: {rule_instance.name}")
        
    @classmethod
    def get_all_rules(cls) -> List[BaseHydrologyRule]:
        return list(cls._rules.values())
