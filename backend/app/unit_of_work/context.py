"""Unit of Work Context Manager."""
import contextvars
from typing import Optional
from app.unit_of_work.interfaces import IUnitOfWork

# Context variable to hold the currently executing Unit of Work.
# This allows deeply nested services or background workers to access 
# the UoW without it being passed explicitly through function signatures.
_current_uow: contextvars.ContextVar[Optional[IUnitOfWork]] = contextvars.ContextVar(
    "current_uow", default=None
)

def set_current_uow(uow: IUnitOfWork) -> contextvars.Token:
    """Injects the UoW into the current async context."""
    return _current_uow.set(uow)

def get_current_uow() -> Optional[IUnitOfWork]:
    """Retrieves the UoW from the current async context."""
    return _current_uow.get()

def reset_current_uow(token: contextvars.Token) -> None:
    """Removes the UoW from the current async context."""
    _current_uow.reset(token)
