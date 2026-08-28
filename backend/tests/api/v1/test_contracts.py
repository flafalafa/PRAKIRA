import pytest
from datetime import datetime, timezone
from app.api.v1.schemas.response import SuccessResponse, PaginatedResponse, ApiMeta
from app.api.v1.schemas.errors import ApiError
from app.api.v1.schemas.pagination import PaginationMeta
from app.api.v1.schemas.error_codes import ErrorCode
from pydantic import ValidationError

def test_success_response_contract():
    resp = SuccessResponse(
        data={"id": "123", "name": "Pondok Aren"},
        request_id="req_123"
    )
    
    dump = resp.model_dump()
    assert "data" in dump
    assert "meta" in dump
    assert "request_id" in dump
    assert "timestamp" in dump
    assert "version" in dump
    
    assert dump["request_id"] == "req_123"
    assert dump["version"] == "v1"
    assert dump["data"]["id"] == "123"

def test_paginated_response_contract():
    pagination = PaginationMeta(
        page=1,
        page_size=20,
        total=100,
        total_pages=5,
        has_next=True,
        has_previous=False
    )
    
    resp = PaginatedResponse(
        data=[{"id": "1"}, {"id": "2"}],
        meta=ApiMeta(pagination=pagination),
        request_id="req_456"
    )
    
    dump = resp.model_dump()
    assert "data" in dump
    assert "meta" in dump
    assert "pagination" in dump["meta"]
    assert dump["meta"]["pagination"]["total"] == 100
    assert dump["request_id"] == "req_456"
    assert dump["version"] == "v1"
    assert len(dump["data"]) == 2

def test_api_error_contract():
    error = ApiError(
        error_code=ErrorCode.AREA_NOT_FOUND.value,
        message="Area not found",
        details={"area_id": "xyz"},
        request_id="req_789",
        path="/api/v1/areas/xyz"
    )
    
    dump = error.model_dump()
    assert dump["error_code"] == "AREA_NOT_FOUND"
    assert dump["message"] == "Area not found"
    assert dump["details"]["area_id"] == "xyz"
    assert dump["request_id"] == "req_789"
    assert dump["path"] == "/api/v1/areas/xyz"
    assert "timestamp" in dump
    assert dump["version"] == "v1"

def test_invalid_pagination():
    with pytest.raises(ValidationError):
        PaginationMeta(page=-1, page_size=20, total=0, total_pages=0, has_next=False, has_previous=False)
