"""Engine Registry."""
from typing import Dict, Any
from app.core.logger import get_logger

logger = get_logger(__name__)

class EngineRegistry:
    _engines: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def register(cls, name: str, engine_class: Any, priority: int = 10, enabled: bool = True) -> None:
        cls._engines[name] = {
            "class": engine_class,
            "priority": priority,
            "enabled": enabled
        }
        logger.debug(f"Registered engine: {name}")
        
    @classmethod
    def get_enabled_engines(cls) -> list:
        active = [(k, v) for k, v in cls._engines.items() if v["enabled"]]
        return sorted(active, key=lambda x: x[1]["priority"])
