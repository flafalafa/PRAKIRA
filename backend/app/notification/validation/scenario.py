"""Validation Scenarios."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel, Field
import uuid

class ScenarioContext(BaseModel):
    scenario_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    expected_outcomes: List[str] = Field(default_factory=list)

class BaseScenario(ABC):
    @property
    @abstractmethod
    def context(self) -> ScenarioContext:
        pass
        
    @abstractmethod
    async def setup(self) -> None:
        pass
        
    @abstractmethod
    async def execute(self) -> Dict[str, Any]:
        """Returns raw simulation results to be validated."""
        pass
        
    @abstractmethod
    async def teardown(self) -> None:
        pass

class WatchNotificationScenario(BaseScenario):
    def __init__(self):
        self._context = ScenarioContext(
            name="WATCH_NOTIFICATION",
            description="Simulates a standard WATCH level notification",
            expected_outcomes=["POLICY_PASSED", "PREFERENCES_PASSED", "DELIVERED"]
        )
        
    @property
    def context(self) -> ScenarioContext:
        return self._context
        
    async def setup(self) -> None:
        pass
        
    async def execute(self) -> Dict[str, Any]:
        return {"status": "DELIVERED", "latency": 150}
        
    async def teardown(self) -> None:
        pass

class EmergencyOverrideScenario(BaseScenario):
    def __init__(self):
        self._context = ScenarioContext(
            name="EMERGENCY_OVERRIDE",
            description="Simulates an EMERGENCY notification bypassing quiet hours",
            expected_outcomes=["QUIET_HOURS_BYPASSED", "DELIVERED_HIGH_PRIORITY"]
        )
        
    @property
    def context(self) -> ScenarioContext:
        return self._context
        
    async def setup(self) -> None:
        pass
        
    async def execute(self) -> Dict[str, Any]:
        return {"status": "DELIVERED", "latency": 50, "priority": "high", "override_active": True}
        
    async def teardown(self) -> None:
        pass
