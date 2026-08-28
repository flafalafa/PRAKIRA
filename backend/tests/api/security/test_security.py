import pytest
from fastapi import FastAPI, Depends, Request
from fastapi.testclient import TestClient
from app.api.security.dependencies import get_current_user, require_role, require_permission
from app.api.security.roles import Role
from app.api.security.permissions import Permission

app = FastAPI()

@app.get("/public")
async def public_route():
    return {"message": "public"}

@app.get("/protected")
async def protected_route(user = Depends(get_current_user)):
    return {"user": user.principal_id}
    
@app.get("/admin")
async def admin_route(user = Depends(require_role(Role.ADMIN))):
    return {"user": user.principal_id}

client = TestClient(app)

def test_public_route():
    resp = client.get("/public")
    assert resp.status_code == 200

def test_protected_route_no_auth():
    resp = client.get("/protected")
    assert resp.status_code == 401

def test_protected_route_invalid_token():
    resp = client.get("/protected", headers={"Authorization": "Bearer invalid_token"})
    assert resp.status_code == 401
    assert "invalid" in resp.json()["detail"].lower()
    
def test_protected_route_expired_token():
    resp = client.get("/protected", headers={"Authorization": "Bearer expired_token"})
    assert resp.status_code == 401
    assert "expired" in resp.json()["detail"].lower()

def test_protected_route_valid_token():
    resp = client.get("/protected", headers={"Authorization": "Bearer valid_user_token"})
    assert resp.status_code == 200
    assert resp.json()["user"] == "user_123"

def test_protected_route_api_key():
    resp = client.get("/protected", headers={"X-API-Key": "valid_api_key"})
    assert resp.status_code == 200
    assert resp.json()["user"] == "service_account"
    
def test_protected_route_invalid_api_key():
    resp = client.get("/protected", headers={"X-API-Key": "wrong"})
    assert resp.status_code == 401

def test_admin_route_forbidden():
    resp = client.get("/admin", headers={"Authorization": "Bearer valid_user_token"})
    assert resp.status_code == 403
