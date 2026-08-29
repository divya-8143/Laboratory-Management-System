import math
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_roles, RoleEnum, get_current_user_payload
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
    PaginatedPatientsResponse
)
from app.services.patient_service import PatientService
from app.core.exceptions import NotFoundException

router = APIRouter(prefix="/patients", tags=["Patient Management"])


@router.get("", response_model=PaginatedPatientsResponse)
async def list_patients(
    search: Optional[str] = Query(None, description="Search by name, phone, code, email"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.RECEPTIONIST, RoleEnum.TECHNICIAN, RoleEnum.DOCTOR])),
    db: AsyncSession = Depends(get_db)
):
    """Search and list patients with pagination."""
    items, total = await PatientService.list_patients(db, search=search, page=page, limit=limit)
    pages = math.ceil(total / limit) if total > 0 else 1
    return PaginatedPatientsResponse(
        items=items,
        total=total,
        page=page,
        pages=pages,
        limit=limit
    )


@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def register_patient(
    patient_in: PatientCreate,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.RECEPTIONIST])),
    db: AsyncSession = Depends(get_db)
):
    """Register a new patient."""
    return await PatientService.create_patient(db, patient_in, creator_id=payload["sub"])


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient_by_id(
    patient_id: str,
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve patient record by ID."""
    patient = await PatientService.get_patient_by_id(db, patient_id)
    if not patient:
        raise NotFoundException("Patient", patient_id)
    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: str,
    patient_in: PatientUpdate,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.RECEPTIONIST])),
    db: AsyncSession = Depends(get_db)
):
    """Update patient demographics or medical notes."""
    return await PatientService.update_patient(db, patient_id, patient_in, actor_id=payload["sub"])
