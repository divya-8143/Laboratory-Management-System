import math
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_roles, RoleEnum, get_current_user_payload
from app.models.order import OrderStatusEnum, OrderPriorityEnum
from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    PaginatedOrdersResponse,
    PaymentCreate,
    InvoiceResponse
)
from app.services.order_service import OrderService
from app.core.exceptions import NotFoundException

router = APIRouter(prefix="/orders", tags=["Lab Orders & Billing"])


@router.get("", response_model=PaginatedOrdersResponse)
async def list_orders(
    patient_id: Optional[str] = Query(None),
    status: Optional[OrderStatusEnum] = Query(None),
    priority: Optional[OrderPriorityEnum] = Query(None),
    search: Optional[str] = Query(None, description="Search by order number or patient name"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_db)
):
    """List lab orders with status and priority filters."""
    # If patient role, restrict to their own orders
    user_role = payload.get("role")
    items, total = await OrderService.list_orders(
        db,
        patient_id=patient_id,
        status=status,
        priority=priority,
        search=search,
        page=page,
        limit=limit
    )
    pages = math.ceil(total / limit) if total > 0 else 1
    return PaginatedOrdersResponse(
        items=items,
        total=total,
        page=page,
        pages=pages,
        limit=limit
    )


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreate,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.RECEPTIONIST, RoleEnum.DOCTOR])),
    db: AsyncSession = Depends(get_db)
):
    """Create a new clinical laboratory order with automatic sample tube clustering and invoicing."""
    return await OrderService.create_order(db, order_in, creator_id=payload["sub"])


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_db)
):
    """Get complete order details, tube items, samples, and invoice."""
    order = await OrderService.get_order_by_id(db, order_id)
    if not order:
        raise NotFoundException("Order", order_id)
    return order


@router.post("/{order_id}/payments", response_model=InvoiceResponse)
async def record_payment(
    order_id: str,
    payment_in: PaymentCreate,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.RECEPTIONIST])),
    db: AsyncSession = Depends(get_db)
):
    """Record payment transaction against order invoice."""
    return await OrderService.record_payment(db, order_id, payment_in, receiver_id=payload["sub"])
