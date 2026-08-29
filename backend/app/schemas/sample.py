from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.catalog import SpecimenTypeEnum, ContainerTypeEnum
from app.models.sample import SampleStatusEnum
from app.schemas.auth import UserResponse


class SampleStatusHistoryResponse(BaseModel):
    id: str
    from_status: Optional[str] = None
    to_status: str
    comments: Optional[str] = None
    timestamp: datetime
    changed_by: Optional[UserResponse] = None

    class Config:
        from_attributes = True


class SampleResponse(BaseModel):
    id: str
    order_id: str
    barcode: str
    specimen_type: SpecimenTypeEnum
    container_type: ContainerTypeEnum
    status: SampleStatusEnum
    collected_at: Optional[datetime] = None
    collected_by_id: Optional[str] = None
    collector: Optional[UserResponse] = None
    received_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    notes: Optional[str] = None
    status_history: List[SampleStatusHistoryResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class SampleCollectionRequest(BaseModel):
    notes: Optional[str] = None


class SampleRejectionRequest(BaseModel):
    reason: str = Field(..., min_length=3, description="Clinical reason for specimen rejection")


class SampleBarcodeInfo(BaseModel):
    sample_id: str
    barcode: str
    patient_name: str
    patient_code: str
    patient_gender_age: str
    specimen_type: str
    container_type: str
    collected_at: Optional[str] = None
