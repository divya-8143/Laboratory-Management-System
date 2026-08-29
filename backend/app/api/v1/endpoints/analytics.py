from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_roles, RoleEnum
from app.schemas.analytics import (
    KPIOverviewResponse,
    MostRequestedTestItem,
    RevenueTrendPoint,
    CategoryDistributionItem
)
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Executive Analytics & Clinical KPIs"])


@router.get("/overview", response_model=KPIOverviewResponse)
async def get_kpi_overview(
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.DOCTOR, RoleEnum.RECEPTIONIST, RoleEnum.TECHNICIAN])),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve executive laboratory metrics (test counts, revenue, TAT, sample pipeline)."""
    return await AnalyticsService.get_overview_kpis(db)


@router.get("/most-requested", response_model=List[MostRequestedTestItem])
async def get_most_requested_tests(
    limit: int = Query(10, ge=1, le=50),
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.DOCTOR])),
    db: AsyncSession = Depends(get_db)
):
    """List most ordered clinical tests with revenue contributions."""
    return await AnalyticsService.get_most_requested_tests(db, limit=limit)


@router.get("/revenue-trends", response_model=List[RevenueTrendPoint])
async def get_revenue_trends(
    period_type: str = Query("daily", pattern="^(daily|monthly)$"),
    payload: dict = Depends(require_roles([RoleEnum.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve time-series financial trend breakdown (daily / monthly)."""
    return await AnalyticsService.get_revenue_trends(db, period_type=period_type)


@router.get("/category-distribution", response_model=List[CategoryDistributionItem])
async def get_category_distribution(
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.DOCTOR])),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve test volume breakdown by clinical department/category."""
    return await AnalyticsService.get_test_category_distribution(db)
