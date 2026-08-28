# Enterprise API Authentication & Security Boundary

This module establishes the security perimeter for the Flood Guardian API. It is responsible for validating who is calling the API (Authentication) and what they are allowed to do (Authorization).

## Architecture
- **Authentication Abstraction (`authentication.py`)**: Defines `BaseAuthenticationProvider`. This allows us to plug in multiple authentication methods (JWT, API Keys, OAuth) without rewriting API routes.
- **Providers (`providers.py`)**: Contains the concrete implementations like `JWTAuthenticationProvider` and `APIKeyAuthenticationProvider`.
- **Security Context (`context.py`)**: Once authenticated, the provider generates a `SecurityContext`. This context is injected into the route and contains the user's ID, roles, and permissions.
- **Policies (`policies.py`)**: Contains pure functions to evaluate if a `SecurityContext` has the necessary roles or permissions to proceed.
- **Dependencies (`dependencies.py`)**: The FastAPI glue. Provides `Depends(get_current_user)`, `Depends(require_role(Role.ADMIN))`, etc.

## Design Philosophy
1. **Deny by Default**: Unless a route explicitly declares itself public (by not including the security dependency), it will reject unauthenticated requests.
2. **No Business Logic**: Security boundaries do not know what a "Flood Prediction" is. They only know about "Permissions" (e.g., `prediction:read`).
3. **Log Sanitization**: Exceptions and loggers in this module intentionally do not print the contents of tokens or API keys to prevent credential leakage.
