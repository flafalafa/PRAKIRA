from app.api.v1.schemas.response import SuccessResponse
from app.api.v1.schemas.common import Meta
from app.api.v1.schemas.errors import ErrorResponse, ErrorDetail

def test_success_response():
    meta = Meta(request_id="123")
    resp = SuccessResponse(data={"foo": "bar"}, meta=meta)
    assert resp.data["foo"] == "bar"
    assert resp.meta.request_id == "123"

def test_error_response():
    error_detail = ErrorDetail(error_code="ERR_001", message="Not found")
    resp = ErrorResponse(error=error_detail, request_id="123")
    assert resp.error.error_code == "ERR_001"
    assert resp.request_id == "123"
