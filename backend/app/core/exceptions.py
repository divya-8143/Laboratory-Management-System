from typing import Any, Optional, Dict
from fastapi import HTTPException, status


class ClinicalLMSException(HTTPException):
    """Base exception for Laboratory Management System errors."""
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundException(ClinicalLMSException):
    def __init__(self, resource_name: str, identifier: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_name} with identifier '{identifier}' was not found."
        )


class UnauthorizedException(ClinicalLMSException):
    def __init__(self, detail: str = "Invalid credentials or authorization token expired."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class ForbiddenException(ClinicalLMSException):
    def __init__(self, detail: str = "You do not have permission to execute this clinical action."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class ConflictException(ClinicalLMSException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class ClinicalValidationError(ClinicalLMSException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )
