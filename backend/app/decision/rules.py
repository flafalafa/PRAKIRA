"""Base class for all Analysis Rules."""
from abc import ABC, abstractmethod
from typing import Any
from app.decision.context import DecisionContext
from app.decision.state import EngineState

class BaseRule(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    async def evaluate(self, context: DecisionContext, state: EngineState) -> bool:
        """Returns True if rule triggered."""
        pass
