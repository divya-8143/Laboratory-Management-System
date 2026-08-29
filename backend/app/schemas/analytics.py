from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.models.audit import AuditActionEnum
from app.schemas.auth import UserResponse


class KPIOverviewResponse(BaseModel):
    total_patients: int
    total_orders: int
    total_tests_conducted: int
    total_revenue: float
    total_collected_revenue: float
    total_outstanding_balance: float
    pending_orders: int
    processing_orders: int
    completed_orders: int
    cancelled_orders: int
    samples_pending_collection: int
    samples_collected: int
    samples_in_lab: int
    samples_rejected: int
    avg_turnaround_time_hours: float


class MostRequestedTestItem(BaseModel):
    test_id: str
    test_code: str
    test_name: str
    category_name: str
    order_count: int
    total_revenue_generated: float


class RevenueTrendPoint(BaseModel):
    period: str  # e.g., "2026-08-25", "Aug 2026", "2026-W34"
    gross_revenue: float
    net_collected: float
    order_count: int


class CategoryDistributionItem(BaseModel):
    category_name: str
    category_code: str
    test_count: int
    percentage: float


class AuditLogResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    user: Optional[UserResponse] = None
    action: AuditActionEnum
    entity_name: str
    entity_id: Optional[str] = None
    details: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True
