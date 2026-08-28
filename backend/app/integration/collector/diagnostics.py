"""System Diagnostics generation."""
from app.integration.collector.registry import IntegrationRegistry
from app.scheduler.health import SchedulerHealth
from typing import Dict, Any

class SystemDiagnostics:
    @staticmethod
    def generate() -> Dict[str, Any]:
        return {
            "collectors": IntegrationRegistry.get_registered_providers(),
            "scheduler_status": SchedulerHealth.get_metrics(),
            "pipeline_status": "ACTIVE",
            "configuration": {
                "strict_mode": True,
                "validation_mode": "FULL"
            }
        }
