from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.result import ResultFlagEnum
from app.schemas.catalog import TestParameterResponse
from app.schemas.auth import UserResponse


class ParameterResultEntry(BaseModel):
    parameter_id: str
    numeric_value: Optional[float] = None
    text_value: Optional[str] = None
    technician_notes: Optional[str] = None


class BatchResultEntryRequest(BaseModel):
    order_item_id: str
    results: List[ParameterResultEntry] = Field(..., min_items=1)


class ResultResponse(BaseModel):
    id: str
    order_item_id: str
    parameter_id: str
    parameter: Optional[TestParameterResponse] = None
    sample_id: str
    numeric_value: Optional[float] = None
    text_value: Optional[str] = None
    formatted_value: str
    flag: ResultFlagEnum
    reference_range_display: Optional[str] = None
    is_abnormal: bool
    is_critical: bool
    technician_notes: Optional[str] = None
    entered_by_id: str
    technician: Optional[UserResponse] = None
    entered_at: datetime

    class Config:
        from_attributes = True


class WorklistItemResponse(BaseModel):
    order_item_id: str
    order_id: str
    order_number: str
    priority: str
    patient_id: str
    patient_name: str
    patient_code: str
    patient_gender: str
    patient_age: int
    test_id: str
    test_code: str
    test_name: str
    sample_barcode: str
    sample_status: str
    item_status: str
    results_count: int
    parameters_count: int
