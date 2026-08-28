"""Validation Context for resolving cross-entity references."""
from typing import Dict, Any, Optional

# Late imports to avoid circular dependencies if entities import context later
from app.domain.entities.area import Area
from app.domain.entities.river import River
from app.domain.entities.flood_prediction import FloodPrediction
from app.domain.entities.flood_event import FloodEvent

class ValidationContext:
    """
    Holds reference data required for cross-entity validation.
    Provides necessary context (e.g. parent entities) to evaluate rules 
    without the Validator itself fetching from the database.
    """
    def __init__(self):
        self.areas: Dict[str, Area] = {}
        self.rivers: Dict[str, River] = {}
        self.predictions: Dict[str, FloodPrediction] = {}
        self.events: Dict[str, FloodEvent] = {}
        self.metadata: Dict[str, Any] = {}
        
    def add_area(self, area: Area):
        self.areas[area.id] = area
        
    def get_area(self, area_id: str) -> Optional[Area]:
        return self.areas.get(area_id)
        
    def add_river(self, river: River):
        self.rivers[river.id] = river
        
    def get_river(self, river_id: str) -> Optional[River]:
        return self.rivers.get(river_id)

    def add_prediction(self, prediction: FloodPrediction):
        self.predictions[prediction.id] = prediction

    def add_event(self, event: FloodEvent):
        self.events[event.id] = event
