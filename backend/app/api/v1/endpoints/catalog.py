from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_roles, RoleEnum, get_current_user_payload
from app.schemas.catalog import (
    TestCategoryCreate,
    TestCategoryResponse,
    TestCreate,
    TestUpdate,
    TestResponse
)
from app.services.catalog_service import CatalogService
from app.core.exceptions import NotFoundException

router = APIRouter(prefix="/catalog", tags=["Test Catalog & Reference Engine"])


@router.get("/categories", response_model=List[TestCategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    """List all active test categories."""
    return await CatalogService.list_categories(db)


@router.post("/categories", response_model=TestCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    cat_in: TestCategoryCreate,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Create a new clinical test category (Admin only)."""
    return await CatalogService.create_category(db, cat_in)


@router.get("/tests", response_model=List[TestResponse])
async def list_tests(
    category_id: Optional[str] = Query(None, description="Filter tests by category"),
    search: Optional[str] = Query(None, description="Search tests by name or code"),
    active_only: bool = Query(True, description="Filter only active tests"),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve test catalog with sub-parameters and reference bounds."""
    return await CatalogService.list_tests(
        db, category_id=category_id, search=search, active_only=active_only
    )


@router.get("/tests/{test_id}", response_model=TestResponse)
async def get_test(test_id: str, db: AsyncSession = Depends(get_db)):
    """Retrieve single test profile with full parameter hierarchies."""
    test = await CatalogService.get_test_by_id(db, test_id)
    if not test:
        raise NotFoundException("Test", test_id)
    return test


@router.post("/tests", response_model=TestResponse, status_code=status.HTTP_201_CREATED)
async def create_test(
    test_in: TestCreate,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Create new clinical test with parameter hierarchies and reference ranges (Admin only)."""
    return await CatalogService.create_test(db, test_in, creator_id=payload["sub"])


@router.put("/tests/{test_id}", response_model=TestResponse)
async def update_test(
    test_id: str,
    test_in: TestUpdate,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Update test attributes or pricing (Admin only)."""
    return await CatalogService.update_test(db, test_id, test_in, actor_id=payload["sub"])
