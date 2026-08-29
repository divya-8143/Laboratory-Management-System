from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_roles, RoleEnum
from app.models.audit import AuditActionEnum
from app.schemas.analytics import AuditLogResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/audit", tags=["Compliance & Audit Logs"])


@router.get("/logs", response_model=List[AuditLogResponse])
async def list_audit_logs(
    action: Optional[AuditActionEnum] = Query(None, description="Filter by clinical action"),
    entity_name: Optional[str] = Query(None, description="Filter by entity e.g. Patient, Order, Sample"),
    user_id: Optional[str] = Query(None, description="Filter by actor user ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    payload: dict = Depends(require_roles([RoleEnum.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve immutable system audit logs for ISO 15189 / HIPAA compliance."""
    return await AnalyticsService.list_audit_logs(
        db, action=action, entity_name=entity_name, user_id=user_id, skip=skip, limit=limit
    )
