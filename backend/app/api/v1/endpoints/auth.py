from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import get_current_user_payload, require_roles, RoleEnum
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    UserResponse,
    PasswordChangeRequest,
    SignatureUploadRequest
)
from app.services.auth_service import AuthService
from app.core.exceptions import UnauthorizedException

router = APIRouter(prefix="/auth", tags=["Authentication & Identity"])


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user with email/password and issue JWT token pair."""
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    user, access_token, refresh_token = await AuthService.authenticate_user(
        db, login_data, ip_address=client_ip, user_agent=user_agent
    )
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """Obtain a new access token using a valid refresh token."""
    user, access_token, refresh_token = await AuthService.refresh_tokens(
        db, refresh_data.refresh_token
    )
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_db)
):
    """Get the authenticated user's profile."""
    user = await AuthService.get_user_by_id(db, payload["sub"])
    if not user:
        raise UnauthorizedException("User profile not found.")
    return user


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    pwd_in: PasswordChangeRequest,
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_db)
):
    """Change the logged in user's password."""
    await AuthService.change_password(db, payload["sub"], pwd_in)
    return {"message": "Password changed successfully."}


@router.post("/signature", response_model=UserResponse)
async def upload_doctor_signature(
    sig_in: SignatureUploadRequest,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.DOCTOR])),
    db: AsyncSession = Depends(get_db)
):
    """Upload digital signature data URL for doctor report signing."""
    user = await AuthService.upload_signature(db, payload["sub"], sig_in.signature_data_url)
    return user
