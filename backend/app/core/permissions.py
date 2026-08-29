import enum
from typing import List, Callable
from fastapi import Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException, ForbiddenException


class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    RECEPTIONIST = "RECEPTIONIST"
    TECHNICIAN = "TECHNICIAN"
    DOCTOR = "DOCTOR"
    PATIENT = "PATIENT"


security_scheme = HTTPBearer(auto_error=False)


async def get_current_user_payload(
    credentials: HTTPAuthorizationCredentials = Security(security_scheme)
) -> dict:
    """Validate Bearer JWT token and return token payload."""
    if not credentials:
        raise UnauthorizedException("Authentication token required.")
    
    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise UnauthorizedException("Invalid or expired access token.")
    
    return payload


def require_roles(allowed_roles: List[RoleEnum]) -> Callable:
    """Dependency factory restricting endpoint access to specific roles."""
    async def role_checker(payload: dict = Depends(get_current_user_payload)) -> dict:
        user_role = payload.get("role")
        if not user_role or user_role not in [role.value for role in allowed_roles]:
            raise ForbiddenException(
                f"Access denied. Required roles: {[r.value for r in allowed_roles]}, user role: '{user_role}'"
            )
        return payload
    return role_checker
