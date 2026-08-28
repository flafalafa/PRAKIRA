"""Radar Rule Registry."""
from typing import Dict, List
from app.decision.radar.rules import BaseRadarRule
from app.core.logger import get_logger

logger = get_logger(__name__)

class RadarRuleRegistry:
    _rules: Dict[str, BaseRadarRule] = {}
    
    @classmethod
    def register(cls, rule_instance: BaseRadarRule) -> None:
        cls._rules[rule_instance.name] = rule_instance
        logger.debug(f"Registered radar rule: {rule_instance.name}")
        
    @classmethod
    def get_all_rules(cls) -> List[BaseRadarRule]:
        return list(cls._rules.values())
