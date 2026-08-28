"""Readiness Report builder."""
from enum import Enum
from typing import Dict, Any, List
from pydantic import BaseModel

class ReadinessStatus(str, Enum):
    READY = "READY"
    PARTIALLY_READY = "PARTIALLY_READY"
    NOT_READY = "NOT_READY"
    UNKNOWN = "UNKNOWN"

class ReadinessReport(BaseModel):
    status: ReadinessStatus
    components_validated: int
    failed_components: List[str]
    diagnostics: Dict[str, Any]
