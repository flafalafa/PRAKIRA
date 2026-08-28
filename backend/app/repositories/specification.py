"""Specification Pattern for Repositories."""
from abc import ABC, abstractmethod
from typing import Any

class Specification(ABC):
    """
    Abstract base class for Query Specifications.
    Allows declarative composition of query filters keeping business logic out of the repository.
    """
    
    @abstractmethod
    def to_expression(self, model: Any) -> Any:
        """Translates the specification into a SQLAlchemy expression."""
        pass

    def __and__(self, other: "Specification") -> "AndSpecification":
        return AndSpecification(self, other)

    def __or__(self, other: "Specification") -> "OrSpecification":
        return OrSpecification(self, other)

    def __invert__(self) -> "NotSpecification":
        return NotSpecification(self)


class AndSpecification(Specification):
    def __init__(self, left: Specification, right: Specification):
        self.left = left
        self.right = right
        
    def to_expression(self, model: Any) -> Any:
        from sqlalchemy import and_
        return and_(self.left.to_expression(model), self.right.to_expression(model))


class OrSpecification(Specification):
    def __init__(self, left: Specification, right: Specification):
        self.left = left
        self.right = right
        
    def to_expression(self, model: Any) -> Any:
        from sqlalchemy import or_
        return or_(self.left.to_expression(model), self.right.to_expression(model))


class NotSpecification(Specification):
    def __init__(self, spec: Specification):
        self.spec = spec
        
    def to_expression(self, model: Any) -> Any:
        from sqlalchemy import not_
        return not_(self.spec.to_expression(model))
