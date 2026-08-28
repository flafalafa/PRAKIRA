"""Filter Registry."""
from typing import Dict, List
from app.notification.preferences.filters import BaseFilter
from app.core.logger import get_logger

logger = get_logger(__name__)

class PreferenceFilterRegistry:
    _filters: Dict[str, BaseFilter] = {}
    
    @classmethod
    def register(cls, filter_obj: BaseFilter) -> None:
        cls._filters[filter_obj.name] = filter_obj
        
    @classmethod
    def get_all(cls) -> List[BaseFilter]:
        return list(cls._filters.values())
