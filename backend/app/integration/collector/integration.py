"""Main Integration Orchestrator."""
from typing import List
from app.integration.collector.registry import IntegrationRegistry
from app.integration.collector.validator import SystemValidator
from app.integration.collector.health import IntegrationHealth
from app.integration.collector.diagnostics import SystemDiagnostics
from app.integration.collector.report import ReadinessReport, ReadinessStatus
from app.core.logger import get_logger

logger = get_logger(__name__)

class EnterpriseIntegration:
    @staticmethod
    async def verify_system_readiness() -> ReadinessReport:
        logger.info("Starting Enterprise System Integration Verification.")
        
        collectors = IntegrationRegistry.get_registered_collectors()
        failed_components = []
        
        # 1. Contract Validation
        for name, collector_class in collectors.items():
            try:
                instance = collector_class()
                SystemValidator.validate_collector_contract(instance)
            except Exception as e:
                logger.error(f"Contract validation failed for {name}: {str(e)}")
                failed_components.append(name)
                
        # 2. Health Check Validation
        health_results = await IntegrationHealth.check_all()
        for name, status in health_results.items():
            if status != "AVAILABLE" and name not in failed_components:
                if status == "UNAVAILABLE":
                    failed_components.append(name)
                    
        # 3. Generate Diagnostics
        diagnostics = SystemDiagnostics.generate()
        
        # Determine Status
        status = ReadinessStatus.READY
        if failed_components:
            if len(failed_components) == len(collectors):
                status = ReadinessStatus.NOT_READY
            else:
                status = ReadinessStatus.PARTIALLY_READY
                
        logger.info(f"Integration Verification Finished. Status: {status}")
        
        return ReadinessReport(
            status=status,
            components_validated=len(collectors),
            failed_components=failed_components,
            diagnostics=diagnostics
        )
