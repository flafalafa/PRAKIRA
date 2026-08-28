"""Unit of Work Factory."""
from app.unit_of_work.base import BaseUnitOfWork
from app.unit_of_work.interfaces import IUnitOfWork

def create_uow() -> IUnitOfWork:
    """
    Creates a new instance of the Unit of Work.
    Abstracts away the concrete implementation allowing easy mocking in unit tests.
    """
    return BaseUnitOfWork()
