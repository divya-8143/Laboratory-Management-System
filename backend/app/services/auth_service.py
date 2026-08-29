import uuid
from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException, status

from app.models.user import User, RoleType
from app.models.audit import AuditLog, AuditActionEnum
from app.schemas.auth import UserCreate, UserUpdate, LoginRequest, PasswordChangeRequest
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.core.exceptions import UnauthorizedException, ConflictException, NotFoundException


class AuthService:
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email.lower().strip()))
        return result.scalars().first()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        login_data: LoginRequest,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Tuple[User, str, str]:
        user = await AuthService.get_user_by_email(db, login_data.email)
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password.")
        
        if not user.is_active:
            raise UnauthorizedException("Account is currently disabled. Please contact the laboratory administrator.")

        # Issue JWT tokens
        access_token = create_access_token(subject=user.id, role=user.role.value)
        refresh_token = create_refresh_token(subject=user.id, role=user.role.value)

        # Audit log login
        audit_entry = AuditLog(
            id=str(uuid.uuid4()),
            user_id=user.id,
            action=AuditActionEnum.LOGIN,
            entity_name="User",
            entity_id=user.id,
            details=f"User {user.email} logged in successfully.",
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(audit_entry)
        await db.commit()

        return user, access_token, refresh_token

    @staticmethod
    async def refresh_tokens(db: AsyncSession, refresh_token: str) -> Tuple[User, str, str]:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid or expired refresh token.")
        
        user_id = payload.get("sub")
        user = await AuthService.get_user_by_id(db, user_id)
        if not user or not user.is_active:
            raise UnauthorizedException("User not found or inactive.")
        
        new_access_token = create_access_token(subject=user.id, role=user.role.value)
        new_refresh_token = create_refresh_token(subject=user.id, role=user.role.value)
        return user, new_access_token, new_refresh_token

    @staticmethod
    async def create_user(
        db: AsyncSession,
        user_in: UserCreate,
        creator_id: Optional[str] = None
    ) -> User:
        existing = await AuthService.get_user_by_email(db, user_in.email)
        if existing:
            raise ConflictException(f"A user with email '{user_in.email}' already exists.")

        user = User(
            id=str(uuid.uuid4()),
            email=user_in.email.lower().strip(),
            hashed_password=get_password_hash(user_in.password),
            first_name=user_in.first_name.strip(),
            last_name=user_in.last_name.strip(),
            role=user_in.role,
            phone=user_in.phone,
            department=user_in.department,
            license_number=user_in.license_number,
            is_active=True
        )
        db.add(user)

        if creator_id:
            audit = AuditLog(
                id=str(uuid.uuid4()),
                user_id=creator_id,
                action=AuditActionEnum.CREATE_PATIENT if user_in.role == RoleType.PATIENT else AuditActionEnum.LOGIN,
                entity_name="User",
                entity_id=user.id,
                details=f"Created user account {user.email} with role {user.role.value}."
            )
            db.add(audit)

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: str,
        user_in: UserUpdate,
        actor_id: Optional[str] = None
    ) -> User:
        user = await AuthService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException("User", user_id)

        update_data = user_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def change_password(
        db: AsyncSession,
        user_id: str,
        pwd_in: PasswordChangeRequest
    ) -> None:
        user = await AuthService.get_user_by_id(db, user_id)
        if not user or not verify_password(pwd_in.old_password, user.hashed_password):
            raise UnauthorizedException("Current password does not match.")

        user.hashed_password = get_password_hash(pwd_in.new_password)
        await db.commit()

    @staticmethod
    async def upload_signature(
        db: AsyncSession,
        user_id: str,
        signature_data_url: str
    ) -> User:
        user = await AuthService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException("User", user_id)

        user.signature_image_url = signature_data_url
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def list_users(
        db: AsyncSession,
        role: Optional[RoleType] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[User]:
        query = select(User)
        if role:
            query = query.where(User.role == role)
        if search:
            search_pattern = f"%{search.strip()}%"
            query = query.where(
                (User.email.ilike(search_pattern)) |
                (User.first_name.ilike(search_pattern)) |
                (User.last_name.ilike(search_pattern))
            )
        query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
