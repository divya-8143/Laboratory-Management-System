from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.order import OrderPriorityEnum, OrderStatusEnum
from app.models.billing import PaymentStatusEnum, PaymentMethodEnum
from app.schemas.patient import PatientResponse
from app.schemas.catalog import TestResponse


class OrderItemCreate(BaseModel):
    test_id: str


class OrderCreate(BaseModel):
    patient_id: str
    referring_doctor: Optional[str] = None
    clinical_notes: Optional[str] = None
    priority: OrderPriorityEnum = OrderPriorityEnum.ROUTINE
    test_ids: List[str] = Field(..., min_items=1)
    discount_amount: float = Field(0.0, ge=0.0)


class OrderItemResponse(BaseModel):
    id: str
    test_id: str
    test: Optional[TestResponse] = None
    sample_id: Optional[str] = None
    price: float
    status: str

    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    amount: float = Field(..., gt=0.0)
    payment_method: PaymentMethodEnum = PaymentMethodEnum.CASH
    transaction_id: Optional[str] = None
    notes: Optional[str] = None


class PaymentResponse(BaseModel):
    id: str
    invoice_id: str
    payment_reference: str
    amount: float
    payment_method: PaymentMethodEnum
    transaction_id: Optional[str] = None
    paid_at: datetime
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    id: str
    invoice_number: str
    subtotal: float
    discount_amount: float
    tax_amount: float
    total_amount: float
    paid_amount: float
    balance_amount: float
    payment_status: PaymentStatusEnum
    payments: List[PaymentResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: str
    order_number: str
    patient_id: str
    patient: Optional[PatientResponse] = None
    referring_doctor: Optional[str] = None
    clinical_notes: Optional[str] = None
    priority: OrderPriorityEnum
    status: OrderStatusEnum
    subtotal: float
    discount_amount: float
    tax_amount: float
    total_amount: float
    order_items: List[OrderItemResponse] = []
    invoice: Optional[InvoiceResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedOrdersResponse(BaseModel):
    items: List[OrderResponse]
    total: int
    page: int
    pages: int
    limit: int
