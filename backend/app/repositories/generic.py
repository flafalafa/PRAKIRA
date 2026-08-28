"""Generic Repository Implementation."""
import math
from typing import Type, TypeVar, Optional, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.repositories.exceptions import EntityNotFoundError, RepositoryError
from app.repositories.pagination import PaginationParams, PaginatedResult, PageMetadata
from app.repositories.sorting import SortingParams, SortDirection
from app.repositories.filters import FilterParams, FilterOperator
from app.repositories.specification import Specification

T = TypeVar("T")
ID = TypeVar("ID")

class GenericRepository(BaseRepository[T, ID]):
    """
    Generic type-safe implementation of IRepository using SQLAlchemy 2.0.
    """
    
    def __init__(self, session: AsyncSession, model_class: Type[T]) -> None:
        super().__init__(session)
        self.model_class = model_class

    async def get_by_id(self, id: ID) -> Optional[T]:
        self.logger.debug("Query Started: get_by_id")
        try:
            stmt = select(self.model_class).where(getattr(self.model_class, "id") == id)
            result = await self.session.execute(stmt)
            entity = result.scalars().first()
            self.logger.debug("Query Finished: get_by_id")
            return entity
        except Exception as e:
            self.logger.error(f"Repository Error during get_by_id: {e}")
            raise RepositoryError(f"Error fetching entity by id: {e}")

    async def exists(self, id: ID) -> bool:
        entity = await self.get_by_id(id)
        return entity is not None

    async def create(self, entity: T) -> T:
        self.logger.debug("Query Started: create")
        try:
            self.session.add(entity)
            await self.session.flush() # Flush to generate ID, commit is handled by TransactionManager
            self.logger.debug("Query Finished: create")
            return entity
        except Exception as e:
            self.logger.error(f"Repository Error during create: {e}")
            raise RepositoryError(f"Error creating entity: {e}")

    async def update(self, entity: T) -> T:
        self.logger.debug("Query Started: update")
        try:
            await self.session.flush()
            self.logger.debug("Query Finished: update")
            return entity
        except Exception as e:
            self.logger.error(f"Repository Error during update: {e}")
            raise RepositoryError(f"Error updating entity: {e}")

    async def delete(self, id: ID) -> None:
        self.logger.debug("Query Started: delete")
        try:
            entity = await self.get_by_id(id)
            if not entity:
                raise EntityNotFoundError(f"Entity with ID {id} not found")
            await self.session.delete(entity)
            await self.session.flush()
            self.logger.debug("Query Finished: delete")
        except EntityNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Repository Error during delete: {e}")
            raise RepositoryError(f"Error deleting entity: {e}")

    async def soft_delete(self, id: ID, user_id: Optional[str] = None) -> None:
        self.logger.debug("Query Started: soft_delete")
        try:
            entity = await self.get_by_id(id)
            if not entity:
                raise EntityNotFoundError(f"Entity with ID {id} not found")
            
            if hasattr(entity, "soft_delete"):
                entity.soft_delete(user_id=user_id)
                await self.session.flush()
            else:
                raise RepositoryError("Entity does not support soft_delete")
            self.logger.debug("Query Finished: soft_delete")
        except (EntityNotFoundError, RepositoryError):
            raise
        except Exception as e:
            self.logger.error(f"Repository Error during soft_delete: {e}")
            raise RepositoryError(f"Error soft deleting entity: {e}")

    async def restore(self, id: ID) -> None:
        self.logger.debug("Query Started: restore")
        try:
            entity = await self.get_by_id(id)
            if not entity:
                raise EntityNotFoundError(f"Entity with ID {id} not found")
                
            if hasattr(entity, "restore"):
                entity.restore()
                await self.session.flush()
            else:
                raise RepositoryError("Entity does not support restore")
            self.logger.debug("Query Finished: restore")
        except (EntityNotFoundError, RepositoryError):
            raise
        except Exception as e:
            self.logger.error(f"Repository Error during restore: {e}")
            raise RepositoryError(f"Error restoring entity: {e}")

    async def count(self, spec: Optional[Specification] = None) -> int:
        stmt = select(func.count()).select_from(self.model_class)
        if spec:
            stmt = stmt.where(spec.to_expression(self.model_class))
        
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def find_one(self, spec: Specification) -> Optional[T]:
        stmt = select(self.model_class).where(spec.to_expression(self.model_class))
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list(
        self,
        filters: Optional[FilterParams] = None,
        sorting: Optional[SortingParams] = None,
        pagination: Optional[PaginationParams] = None,
        spec: Optional[Specification] = None,
        include_deleted: bool = False
    ) -> PaginatedResult[T]:
        self.logger.debug("Query Started: list")
        try:
            stmt = select(self.model_class)
            
            # Handle Soft Delete globally for lists
            if not include_deleted and hasattr(self.model_class, "is_deleted"):
                stmt = stmt.where(getattr(self.model_class, "is_deleted") == False)

            # Handle Specification
            if spec:
                stmt = stmt.where(spec.to_expression(self.model_class))
            
            # Handle Generic Filters
            if filters:
                for f in filters.criteria:
                    col = getattr(self.model_class, f.field, None)
                    if col is not None:
                        if f.operator == FilterOperator.EQ:
                            stmt = stmt.where(col == f.value)
                        elif f.operator == FilterOperator.NEQ:
                            stmt = stmt.where(col != f.value)
                        elif f.operator == FilterOperator.GT:
                            stmt = stmt.where(col > f.value)
                        elif f.operator == FilterOperator.LT:
                            stmt = stmt.where(col < f.value)
                        elif f.operator == FilterOperator.CONTAINS:
                            stmt = stmt.where(col.contains(f.value))
                        elif f.operator == FilterOperator.IN:
                            stmt = stmt.where(col.in_(f.value))
                        # Other operators can be expanded as needed

            # Handle Sorting
            if sorting:
                for order in sorting.orders:
                    col = getattr(self.model_class, order.field, None)
                    if col is not None:
                        if order.direction == SortDirection.DESC:
                            stmt = stmt.order_by(col.desc())
                        else:
                            stmt = stmt.order_by(col.asc())

            # Get Total Count (Subquery approach for accurate complex counts)
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total_items_res = await self.session.execute(count_stmt)
            total_items = total_items_res.scalar() or 0

            # Handle Pagination
            if pagination:
                stmt = stmt.offset(pagination.offset).limit(pagination.page_size)
            
            result = await self.session.execute(stmt)
            items = result.scalars().all()
            
            # Construct Metadata
            page = pagination.page if pagination else 1
            page_size = pagination.page_size if pagination else len(items)
            total_pages = math.ceil(total_items / page_size) if page_size > 0 else 1
            
            metadata = PageMetadata(
                total_items=total_items,
                total_pages=total_pages,
                current_page=page,
                page_size=page_size,
                has_next=page < total_pages,
                has_previous=page > 1
            )
            
            self.logger.debug("Query Finished: list")
            return PaginatedResult(items=list(items), metadata=metadata)
            
        except Exception as e:
            self.logger.error(f"Repository Error during list: {e}")
            raise RepositoryError(f"Error listing entities: {e}")
