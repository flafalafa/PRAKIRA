"""Hydrology Analyzer core component."""
from app.decision.hydrology.context import HydrologyContext
from app.decision.hydrology.registry import HydrologyRuleRegistry
from app.core.logger import get_logger
from typing import List

logger = get_logger(__name__)

class HydrologyAnalyzer:
    @staticmethod
    async def execute_rules(context: HydrologyContext) -> List[str]:
        triggered = []
        rules = HydrologyRuleRegistry.get_all_rules()
        for rule in rules:
            try:
                is_triggered = await rule.evaluate(context)
                if is_triggered:
                    triggered.append(rule.name)
            except Exception as e:
                logger.error(f"Hydrology Rule {rule.name} failed: {str(e)}")
        return triggered
