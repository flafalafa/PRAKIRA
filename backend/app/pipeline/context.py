"""Pipeline Execution Context."""
from datetime import datetime, timezone
from typing import Dict, Any, List

class PipelineContext:
    def __init__(self, trace_id: str, provider_id: str):
        self.trace_id = trace_id
        self.provider_id = provider_id
        self.start_time = datetime.now(timezone.utc)
        self.processing_metadata: Dict[str, Any] = {}
        self.errors: List[str] = []
        
    def add_error(self, step: str, message: str):
        self.errors.append(f"[{step}] {message}")
