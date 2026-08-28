"""Application bootstrap process for Dependency Injection."""
import logging
from app.core.registry import register_dependencies
from app.core.container import container
from app.core.interfaces import IConfiguration, ILogger, IDatabase

# Using standard logger here to bootstrap our internal logger later
logger = logging.getLogger(__name__)

def bootstrap_di() -> None:
    """Initialize container and validate registrations."""
    logger.info("Bootstrapping Dependency Injection Container...")
    
    try:
        # 1. Register all providers
        register_dependencies()
        
        # 2. Validate mandatory registrations
        mandatory_interfaces = [IConfiguration, ILogger, IDatabase]
        for interface in mandatory_interfaces:
            if not container.is_registered(interface):
                raise RuntimeError(f"DI Validation Failed: Mandatory dependency {interface.__name__} is missing.")
                
        # Simple Circular Dependency detection logic could go here in the future
                
        logger.info(f"Successfully registered {len(container._registrations)} core dependencies.")
        
    except Exception as e:
        logger.critical(f"DI Bootstrap Failed: {str(e)}")
        raise e
