"""Sorting support."""
from enum import Enum
from typing import List
from pydantic import BaseModel

class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"

class SortOrder(BaseModel):
    """Represents a sorting directive for a specific field."""
    field: str
    direction: SortDirection = SortDirection.ASC

class SortingParams(BaseModel):
    """Parameters containing multiple sort orders."""
    orders: List[SortOrder] = []
