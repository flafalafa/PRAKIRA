"""Weather Analyzer core component."""
from app.decision.weather.context import WeatherContext
from app.decision.weather.registry import WeatherRuleRegistry
from app.core.logger import get_logger
from typing import List

logger = get_logger(__name__)

class WeatherAnalyzer:
    @staticmethod
    async def execute_rules(context: WeatherContext) -> List[str]:
        triggered = []
        rules = WeatherRuleRegistry.get_all_rules()
        for rule in rules:
            try:
                is_triggered = await rule.evaluate(context)
                if is_triggered:
                    triggered.append(rule.name)
            except Exception as e:
                logger.error(f"Weather Rule {rule.name} failed: {str(e)}")
        return triggered
