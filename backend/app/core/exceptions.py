from app.exceptions.base import AppException
from app.exceptions.not_found import NotFoundException as NotFoundError
from app.exceptions.authorization import AuthorizationException as ForbiddenError

# Aliases for backward compatibility
AppBaseException = AppException
BaseDomainException = AppException
