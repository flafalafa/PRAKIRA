"""Unit of Work Manager and FastAPI Integrations."""
from typing import AsyncGenerator
from app.unit_of_work.interfaces import IUnitOfWork
from app.unit_of_work.factory import create_uow
from app.unit_of_work.context import set_current_uow, reset_current_uow

async def get_uow_dependency() -> AsyncGenerator[IUnitOfWork, None]:
    """
    FastAPI Depends() generator for the Unit of Work.
    Provides a cleanly scoped UoW lifecycle per HTTP request.
    
    Usage:
        @router.post("/process")
        async def process_data(uow: IUnitOfWork = Depends(get_uow_dependency)):
            ...
    """
    uow = create_uow()
    
    # Enter the transactional boundary
    async with uow:
        # Inject into context for background jobs passing through HTTP
        token = set_current_uow(uow)
        try:
            yield uow
        finally:
            reset_current_uow(token)
