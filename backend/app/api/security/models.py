"""Security Models."""
from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub: str
    exp: int
    iat: int
    iss: str
    aud: str
    roles: list[str] = []
    permissions: list[str] = []
