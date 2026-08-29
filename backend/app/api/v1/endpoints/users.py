from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_roles, RoleEnum
from app.models.user import RoleType
from app.schemas.auth import UserCreate, UserUpdate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["User Administration (Admin Only)"])


@router.get("", response_model=List[UserResponse])
async def list_users(
    role: Optional[RoleType] = Query(None, description="Filter users by system role"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    payload: dict = Depends(require_roles([RoleEnum.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """List system users with filtering and search."""
    return await AuthService.list_users(db, role=role, search=search, skip=skip, limit=limit)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Create a new staff or user account."""
    return await AuthService.create_user(db, user_in, creator_id=payload["sub"])


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Get user details by ID."""
    return await AuthService.get_user_by_id(db, user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_in: UserUpdate,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Update user attributes, role, or active status."""
    return await AuthService.update_user(db, user_id, user_in, actor_id=payload["sub"])
