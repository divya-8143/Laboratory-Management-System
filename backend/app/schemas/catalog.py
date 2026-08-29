from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.catalog import SpecimenTypeEnum, ContainerTypeEnum, ParameterDataTypeEnum


class ReferenceRangeBase(BaseModel):
    gender: str = "BOTH"  # "MALE", "FEMALE", "BOTH"
    age_min_days: int = 0
    age_max_days: int = 43800  # ~120 years
    normal_min: Optional[float] = None
    normal_max: Optional[float] = None
    critical_low: Optional[float] = None
    critical_high: Optional[float] = None
    qualitative_normal: Optional[str] = None
    interpretation_text: Optional[str] = None


class ReferenceRangeCreate(ReferenceRangeBase):
    pass


class ReferenceRangeResponse(ReferenceRangeBase):
    id: str
    parameter_id: str

    class Config:
        from_attributes = True


class TestParameterBase(BaseModel):
    parameter_code: str
    name: str
    unit: Optional[str] = None
    data_type: ParameterDataTypeEnum = ParameterDataTypeEnum.NUMERIC
    display_order: int = 0
    formula_expression: Optional[str] = None
    is_active: bool = True


class TestParameterCreate(TestParameterBase):
    reference_ranges: Optional[List[ReferenceRangeCreate]] = []


class TestParameterResponse(TestParameterBase):
    id: str
    test_id: str
    reference_ranges: List[ReferenceRangeResponse] = []

    class Config:
        from_attributes = True


class TestCategoryBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    display_order: int = 0
    is_active: bool = True


class TestCategoryCreate(TestCategoryBase):
    pass


class TestCategoryResponse(TestCategoryBase):
    id: str

    class Config:
        from_attributes = True


class TestBase(BaseModel):
    test_code: str
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    specimen_type: SpecimenTypeEnum
    container_type: ContainerTypeEnum
    price: float = Field(..., ge=0.0)
    turnaround_time_hours: int = 24
    is_active: bool = True


class TestCreate(TestBase):
    category_id: str
    parameters: Optional[List[TestParameterCreate]] = []


class TestUpdate(BaseModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    specimen_type: Optional[SpecimenTypeEnum] = None
    container_type: Optional[ContainerTypeEnum] = None
    price: Optional[float] = None
    turnaround_time_hours: Optional[int] = None
    is_active: Optional[bool] = None


class TestResponse(TestBase):
    id: str
    category_id: str
    category: Optional[TestCategoryResponse] = None
    parameters: List[TestParameterResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
