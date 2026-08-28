"""Scenario Registry."""
from typing import Dict, List
from app.decision.validation.scenario import ValidationScenario

class ScenarioRegistry:
    _scenarios: Dict[str, ValidationScenario] = {}

    @classmethod
    def register(cls, scenario: ValidationScenario) -> None:
        cls._scenarios[scenario.name] = scenario

    @classmethod
    def get_all(cls) -> List[ValidationScenario]:
        return list(cls._scenarios.values())
