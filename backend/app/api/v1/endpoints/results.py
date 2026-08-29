from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_roles, RoleEnum, get_current_user_payload
from app.schemas.result import (
    BatchResultEntryRequest,
    ResultResponse,
    WorklistItemResponse
)
from app.services.result_service import ResultService

router = APIRouter(prefix="/results", tags=["Lab Worklist & Result Entry"])


@router.get("/worklist", response_model=List[WorklistItemResponse])
async def get_worklist(
    status: Optional[str] = Query(None, description="Filter by item status e.g. PENDING, RESULTED"),
    search: Optional[str] = Query(None, description="Search barcode, order, test, patient"),
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.TECHNICIAN, RoleEnum.DOCTOR])),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve laboratory technician testing worklist sorted by clinical priority (STAT first)."""
    return await ResultService.get_technician_worklist(db, status=status, search=search)


@router.post("/batch-entry", response_model=List[ResultResponse])
async def enter_batch_results(
    batch_in: BatchResultEntryRequest,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.TECHNICIAN, RoleEnum.DOCTOR])),
    db: AsyncSession = Depends(get_db)
):
    """
    Enter batch parameter results with real-time biological range evaluation,
    critical/high/low flag calculation, and audit trail generation.
    """
    return await ResultService.enter_batch_results(db, batch_in, technician_id=payload["sub"])


@router.get("/order/{order_id}", response_model=List[ResultResponse])
async def get_order_results(
    order_id: str,
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_db)
):
    """Get all parameter results for an entire order."""
    return await ResultService.get_results_for_order(db, order_id)
