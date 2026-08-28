"""Domain Business Policies."""
from abc import ABC, abstractmethod
from typing import Any
from app.domain.validation.base import ValidationResult
from app.domain.validation.context import ValidationContext

class BaseDomainPolicy(ABC):
    @abstractmethod
    def evaluate(self, entity: Any, context: ValidationContext) -> ValidationResult:
        pass

class AreaRiverConstraintPolicy(BaseDomainPolicy):
    """
    Invariant: River cannot become ACTIVE if Area is inactive.
    """
    def evaluate(self, river: Any, context: ValidationContext) -> ValidationResult:
        result = ValidationResult()
        
        # If the context does not have the area, we assume the repository will handle foreign keys,
        # but for pure domain invariants, the context *should* be populated by application services.
        area = context.get_area(river.area_id)
        if not area:
            # We don't fail immediately, but log a warning or missing context error
            result.add_warning("AREA_NOT_IN_CONTEXT", f"Area {river.area_id} not provided for River validation.")
            return result
            
        from app.domain.entities.river import RiverStatus
        from app.domain.entities.area import AreaStatus
        
        if river.status != RiverStatus.INACTIVE and area.status != AreaStatus.ACTIVE:
            result.add_error(
                "INVALID_RIVER_ACTIVATION", 
                "River cannot be active if its Area is not active."
            )
            
        return result

class ActiveRiverArchiveConstraintPolicy(BaseDomainPolicy):
    """
    Invariant: Area cannot be archived while active Rivers exist.
    """
    def evaluate(self, area: Any, context: ValidationContext) -> ValidationResult:
        result = ValidationResult()
        from app.domain.entities.area import AreaStatus
        from app.domain.entities.river import RiverStatus
        
        if area.status == AreaStatus.ARCHIVED:
            # Check context for rivers belonging to this area
            active_rivers = [
                r for r in context.rivers.values() 
                if r.area_id == area.id and r.status != RiverStatus.INACTIVE
            ]
            if active_rivers:
                result.add_error(
                    "AREA_ARCHIVE_DENIED", 
                    "Cannot archive Area with active Rivers."
                )
                
        return result
        
class PredictionTimelinePolicy(BaseDomainPolicy):
    """
    Invariant: Prediction must precede Flood Event. 
    (Optionally: Rainfall observation must precede Prediction).
    """
    def evaluate(self, event: Any, context: ValidationContext) -> ValidationResult:
        result = ValidationResult()
        
        if hasattr(event, 'prediction_id') and event.prediction_id:
            prediction = context.predictions.get(event.prediction_id)
            if not prediction:
                result.add_warning("PREDICTION_NOT_IN_CONTEXT", "Referenced prediction not loaded in context.")
            else:
                if prediction.prediction_time.value > event.event_start_time.value:
                    result.add_error(
                        "TIMELINE_VIOLATION", 
                        "Prediction time cannot be after Flood Event start time."
                    )
        return result
