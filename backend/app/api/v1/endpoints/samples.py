from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_roles, RoleEnum, get_current_user_payload
from app.models.sample import SampleStatusEnum
from app.schemas.sample import (
    SampleResponse,
    SampleCollectionRequest,
    SampleRejectionRequest,
    SampleBarcodeInfo
)
from app.services.sample_service import SampleService
from app.core.exceptions import NotFoundException

router = APIRouter(prefix="/samples", tags=["Phlebotomy & Sample Tracking"])


@router.get("/queue", response_model=List[SampleResponse])
async def list_samples_queue(
    status: Optional[SampleStatusEnum] = Query(None),
    search: Optional[str] = Query(None, description="Search barcode, order number, patient"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.RECEPTIONIST, RoleEnum.TECHNICIAN, RoleEnum.DOCTOR])),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve phlebotomy sample queue and laboratory accessioning worklist."""
    return await SampleService.list_samples_queue(db, status=status, search=search, skip=skip, limit=limit)


@router.get("/barcode/{barcode}", response_model=SampleResponse)
async def get_sample_by_barcode(
    barcode: str,
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_db)
):
    """Lookup sample tube by scanned barcode."""
    sample = await SampleService.get_sample_by_barcode(db, barcode)
    if not sample:
        raise NotFoundException("Sample barcode", barcode)
    return sample


@router.get("/{sample_id}", response_model=SampleResponse)
async def get_sample(
    sample_id: str,
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve sample details and full lifecycle audit trail."""
    sample = await SampleService.get_sample_by_id(db, sample_id)
    if not sample:
        raise NotFoundException("Sample", sample_id)
    return sample


@router.post("/{sample_id}/collect", response_model=SampleResponse)
async def collect_sample(
    sample_id: str,
    col_in: SampleCollectionRequest,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.TECHNICIAN, RoleEnum.RECEPTIONIST])),
    db: AsyncSession = Depends(get_db)
):
    """Mark specimen collected by phlebotomist."""
    return await SampleService.mark_sample_collected(
        db, sample_id, collector_id=payload["sub"], notes=col_in.notes
    )


@router.post("/{sample_id}/receive", response_model=SampleResponse)
async def receive_sample(
    sample_id: str,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.TECHNICIAN])),
    db: AsyncSession = Depends(get_db)
):
    """Accession specimen into testing laboratory."""
    return await SampleService.mark_sample_received(db, sample_id, technician_id=payload["sub"])


@router.post("/{sample_id}/reject", response_model=SampleResponse)
async def reject_sample(
    sample_id: str,
    rej_in: SampleRejectionRequest,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.TECHNICIAN])),
    db: AsyncSession = Depends(get_db)
):
    """Reject compromised specimen (hemolyzed, clotted, quantity not sufficient)."""
    return await SampleService.reject_sample(
        db, sample_id, reason=rej_in.reason, actor_id=payload["sub"]
    )
