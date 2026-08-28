"""Scenario Registry."""
from typing import Dict, List
from app.notification.validation.scenario import BaseScenario
from app.core.logger import get_logger

logger = get_logger(__name__)

class ScenarioRegistry:
    _scenarios: Dict[str, BaseScenario] = {}
    
    @classmethod
    def register(cls, scenario: BaseScenario) -> None:
        cls._scenarios[scenario.context.name] = scenario
        
    @classmethod
    def get_all(cls) -> List[BaseScenario]:
        return list(cls._scenarios.values())
        
    @classmethod
    def get(cls, name: str) -> BaseScenario:
        return cls._scenarios.get(name)
