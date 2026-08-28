"""Pagination Schemas."""
from pydantic import BaseModel

class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool
