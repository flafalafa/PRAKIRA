"""Risk Rule Registry."""
from typing import Dict, List
from app.decision.risk.rules import BaseRiskRule
from app.core.logger import get_logger

logger = get_logger(__name__)

class RiskRuleRegistry:
    _rules: Dict[str, BaseRiskRule] = {}
    
    @classmethod
    def register(cls, rule_instance: BaseRiskRule) -> None:
        cls._rules[rule_instance.name] = rule_instance
        logger.debug(f"Registered risk rule: {rule_instance.name}")
        
    @classmethod
    def get_all_rules(cls) -> List[BaseRiskRule]:
        return list(cls._rules.values())
