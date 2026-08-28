"""Pipeline specific exceptions."""
from app.core.exceptions import AppBaseException

class PipelineException(AppBaseException):
    pass

class SchemaValidationFailed(PipelineException):
    pass

class TransformationFailed(PipelineException):
    pass

class NormalizationFailed(PipelineException):
    pass

class QualityValidationFailed(PipelineException):
    pass

class CanonicalMappingFailed(PipelineException):
    pass
