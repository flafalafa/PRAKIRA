"""Explanation Generation Models."""
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ReasonSummary(BaseModel):
    rule_name: str
    description: str
    impact: float

class DecisionExplanation(BaseModel):
    reasons: List[ReasonSummary] = Field(default_factory=list)
    supporting_data_refs: List[str] = Field(default_factory=list)
    confidence_summary: str = ""
    missing_data: List[str] = Field(default_factory=list)
