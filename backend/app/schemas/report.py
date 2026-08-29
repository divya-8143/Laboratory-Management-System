from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.report import ReportStatusEnum
from app.schemas.auth import UserResponse


class ReportVerificationRequest(BaseModel):
    pathologist_comments: Optional[str] = None
    clinical_interpretation: Optional[str] = None


class ReportResponse(BaseModel):
    id: str
    order_id: str
    report_number: str
    status: ReportStatusEnum
    verified_by_doctor_id: Optional[str] = None
    verified_by_doctor: Optional[UserResponse] = None
    verified_at: Optional[datetime] = None
    pathologist_comments: Optional[str] = None
    clinical_interpretation: Optional[str] = None
    pdf_filename: Optional[str] = None
    verification_qr_hash: str
    download_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReportVerificationPublicInfo(BaseModel):
    report_number: str
    status: str
    verified_at: Optional[datetime] = None
    verified_by: Optional[str] = None
    patient_initials: str
    patient_code: str
    order_number: str
    tests_included: List[str] = []
    is_authentic: bool = True
    laboratory_name: str
