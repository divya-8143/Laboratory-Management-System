from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from app.models.patient import GenderEnum, BloodGroupEnum


class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: GenderEnum
    blood_group: BloodGroupEnum = BloodGroupEnum.UNKNOWN
    phone: str = Field(..., min_length=5, max_length=50)
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    medical_history_notes: Optional[str] = None
    allergies: Optional[str] = None


class PatientCreate(PatientBase):
    create_portal_account: bool = False
    portal_password: Optional[str] = None


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[GenderEnum] = None
    blood_group: Optional[BloodGroupEnum] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    medical_history_notes: Optional[str] = None
    allergies: Optional[str] = None


class PatientResponse(PatientBase):
    id: str
    patient_code: str
    user_id: Optional[str] = None
    age_years: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedPatientsResponse(BaseModel):
    items: List[PatientResponse]
    total: int
    page: int
    pages: int
    limit: int
