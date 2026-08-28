"""Validator Registry linking entities to their validator pipelines."""
from typing import Dict, Type
from app.domain.validation.validator import DomainValidator
from app.domain.validation.policies import (
    AreaRiverConstraintPolicy, ActiveRiverArchiveConstraintPolicy, PredictionTimelinePolicy
)
from app.domain.validation.rules import (
    check_prediction_confidence, check_event_verification_dependency
)
from app.domain.entities.area import Area
from app.domain.entities.river import River
from app.domain.entities.flood_prediction import FloodPrediction
from app.domain.entities.flood_event import FloodEvent

class ValidatorRegistry:
    """Central registry of all domain validators."""
    
    _validators: Dict[Type, DomainValidator] = {}
    
    @classmethod
    def setup(cls):
        # Register Area Validator
        cls._validators[Area] = DomainValidator(
            policies=[ActiveRiverArchiveConstraintPolicy()]
        )
        
        # Register River Validator
        cls._validators[River] = DomainValidator(
            policies=[AreaRiverConstraintPolicy()]
        )
        
        # Register Prediction Validator
        cls._validators[FloodPrediction] = DomainValidator(
            policies=[],
            rules=[check_prediction_confidence]
        )
        
        # Register FloodEvent Validator
        cls._validators[FloodEvent] = DomainValidator(
            policies=[PredictionTimelinePolicy()],
            rules=[check_event_verification_dependency]
        )
        
    @classmethod
    def get_validator(cls, entity_type: Type) -> DomainValidator:
        if not cls._validators:
            cls.setup()
        return cls._validators.get(entity_type, DomainValidator(policies=[]))
