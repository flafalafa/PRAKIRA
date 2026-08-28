"""Pagination support."""
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")

class PageMetadata(BaseModel):
    """Metadata for paginated results."""
    total_items: int
    total_pages: int
    current_page: int
    page_size: int
    has_next: bool
    has_previous: bool

class PaginatedResult(BaseModel, Generic[T]):
    """Standard paginated result container."""
    items: List[T]
    metadata: PageMetadata

class PaginationParams(BaseModel):
    """Parameters for offset pagination."""
    page: int = 1
    page_size: int = 20
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
