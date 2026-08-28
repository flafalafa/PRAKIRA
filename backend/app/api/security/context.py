"""Security Context."""
from pydantic import BaseModel, Field
from typing import List, Optional
from app.api.security.roles import Role
from app.api.security.permissions import Permission

class SecurityContext(BaseModel):
    principal_id: str
    principal_type: str
    authentication_method: str
    roles: List[Role] = Field(default_factory=list)
    permissions: List[Permission] = Field(default_factory=list)
    scopes: List[str] = Field(default_factory=list)
    token_metadata: dict = Field(default_factory=dict)
    
    @property
    def is_authenticated(self) -> bool:
        return self.principal_id != "anonymous"
