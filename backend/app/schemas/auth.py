from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from app.models.user import RoleType


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    first_name: str
    last_name: str
    role: RoleType


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: RoleType = RoleType.PATIENT
    phone: Optional[str] = None
    department: Optional[str] = None
    license_number: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    license_number: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[RoleType] = None


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)


class SignatureUploadRequest(BaseModel):
    signature_data_url: str  # Base64 data URL e.g. data:image/png;base64,...


class UserResponse(UserBase):
    id: str
    is_active: bool
    signature_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
