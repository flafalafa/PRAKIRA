"""Radar Analyzer core component."""
from app.decision.radar.context import RadarContext
from app.decision.radar.registry import RadarRuleRegistry
from app.core.logger import get_logger
from typing import List, Dict, Any

logger = get_logger(__name__)

class RadarAnalyzer:
    @staticmethod
    async def execute_rules(context: RadarContext, analysis_data: Dict[str, Any]) -> List[str]:
        triggered = []
        rules = RadarRuleRegistry.get_all_rules()
        for rule in rules:
            try:
                is_triggered = await rule.evaluate(context, analysis_data)
                if is_triggered:
                    triggered.append(rule.name)
            except Exception as e:
                logger.error(f"Radar Rule {rule.name} failed: {str(e)}")
        return triggered
