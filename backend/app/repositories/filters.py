"""Generic filtering support."""
from enum import Enum
from typing import Any, List
from pydantic import BaseModel

class FilterOperator(str, Enum):
    """Standard operators for repository filtering."""
    EQ = "eq"
    NEQ = "neq"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NOT_IN = "not_in"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"
    BETWEEN = "between"

class FilterCriteria(BaseModel):
    """Represents a single generic filter criterion."""
    field: str
    operator: FilterOperator
    value: Any

class FilterParams(BaseModel):
    """Collection of filters to apply to a repository query."""
    criteria: List[FilterCriteria] = []
