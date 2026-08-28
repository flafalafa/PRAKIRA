"""Weather Rule Registry."""
from typing import Dict, List
from app.decision.weather.rules import BaseWeatherRule
from app.core.logger import get_logger

logger = get_logger(__name__)

class WeatherRuleRegistry:
    _rules: Dict[str, BaseWeatherRule] = {}
    
    @classmethod
    def register(cls, rule_instance: BaseWeatherRule) -> None:
        cls._rules[rule_instance.name] = rule_instance
        logger.debug(f"Registered weather rule: {rule_instance.name}")
        
    @classmethod
    def get_all_rules(cls) -> List[BaseWeatherRule]:
        return list(cls._rules.values())
