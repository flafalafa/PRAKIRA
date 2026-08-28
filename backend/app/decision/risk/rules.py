"""Risk Analysis Rules & Recommendations."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.decision.risk.context import RiskContext

class BaseRiskRule(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    async def evaluate(self, context: RiskContext, risk_data: Dict[str, Any]) -> bool:
        pass
        
    @abstractmethod
    def get_recommendation(self) -> str:
        pass

class CriticalCapacityRule(BaseRiskRule):
    name = "CRITICAL_CAPACITY_RISK"
    
    async def evaluate(self, context: RiskContext, risk_data: Dict[str, Any]) -> bool:
        factors = risk_data.get("factors", {})
        return factors.get("river_capacity_usage", 0.0) >= 100.0
        
    def get_recommendation(self) -> str:
        return "Immediate Evacuation Recommended"

class CompoundRiskRule(BaseRiskRule):
    name = "COMPOUND_RISK"
    
    async def evaluate(self, context: RiskContext, risk_data: Dict[str, Any]) -> bool:
        factors = risk_data.get("factors", {})
        return (factors.get("river_capacity_usage", 0.0) >= 80.0 and 
                factors.get("rainfall_intensity", 0.0) >= 10.0)
                
    def get_recommendation(self) -> str:
        return "Prepare Vehicle Relocation"
