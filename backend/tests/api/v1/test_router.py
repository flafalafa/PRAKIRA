import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.api.v1.router import api_v1_router

app = FastAPI()
app.include_router(api_v1_router)
client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["status"] == "OK"
    assert "meta" in data
    assert "request_id" in data["meta"]

def test_system_info():
    response = client.get("/api/v1/system/info")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "version" in data["data"]
