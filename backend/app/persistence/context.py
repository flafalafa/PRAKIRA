"""Context management for database sessions."""
import contextvars
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

# Context variable to hold the current database session.
# This allows deep repositories or background workers to access 
# the active session without explicit passing (Dependency Injection).
_current_session: contextvars.ContextVar[Optional[AsyncSession]] = contextvars.ContextVar(
    "current_session", default=None
)

def set_current_session(session: AsyncSession) -> contextvars.Token:
    """Sets the current session in the context."""
    return _current_session.set(session)

def get_current_session() -> Optional[AsyncSession]:
    """Retrieves the current session from the context."""
    return _current_session.get()

def reset_current_session(token: contextvars.Token) -> None:
    """Resets the session context."""
    _current_session.reset(token)
