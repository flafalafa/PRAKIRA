from app.api.v1.schemas.pagination import PaginationMeta
from app.api.v1.schemas.response import PaginatedResponse
from app.api.v1.schemas.common import Meta

def test_paginated_response():
    meta = Meta(request_id="123")
    pagination = PaginationMeta(
        page=1,
        page_size=10,
        total=5,
        total_pages=1,
        has_next=False,
        has_previous=False
    )
    resp = PaginatedResponse(data=[1, 2, 3], pagination=pagination, meta=meta)
    assert len(resp.data) == 3
    assert resp.pagination.total == 5
    assert resp.meta.request_id == "123"
