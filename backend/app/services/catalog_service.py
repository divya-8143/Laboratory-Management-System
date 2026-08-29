import uuid
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.catalog import TestCategory, Test, TestParameter, ReferenceRange
from app.models.audit import AuditLog, AuditActionEnum
from app.schemas.catalog import (
    TestCategoryCreate,
    TestCreate,
    TestUpdate,
    TestParameterCreate,
    ReferenceRangeCreate
)
from app.core.exceptions import NotFoundException, ConflictException


class CatalogService:
    @staticmethod
    async def list_categories(db: AsyncSession) -> List[TestCategory]:
        result = await db.execute(select(TestCategory).order_by(TestCategory.display_order))
        return list(result.scalars().all())

    @staticmethod
    async def create_category(db: AsyncSession, cat_in: TestCategoryCreate) -> TestCategory:
        existing = await db.execute(select(TestCategory).where(TestCategory.code == cat_in.code.upper()))
        if existing.scalars().first():
            raise ConflictException(f"Category code '{cat_in.code}' already exists.")

        category = TestCategory(
            id=str(uuid.uuid4()),
            name=cat_in.name,
            code=cat_in.code.upper(),
            description=cat_in.description,
            display_order=cat_in.display_order,
            is_active=cat_in.is_active
        )
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def list_tests(
        db: AsyncSession,
        category_id: Optional[str] = None,
        search: Optional[str] = None,
        active_only: bool = True
    ) -> List[Test]:
        query = (
            select(Test)
            .options(
                selectinload(Test.category),
                selectinload(Test.parameters).selectinload(TestParameter.reference_ranges)
            )
        )
        if category_id:
            query = query.where(Test.category_id == category_id)
        if active_only:
            query = query.where(Test.is_active.is_(True))
        if search:
            pattern = f"%{search.strip()}%"
            query = query.where(
                (Test.name.ilike(pattern)) |
                (Test.test_code.ilike(pattern)) |
                (Test.short_name.ilike(pattern))
            )

        query = query.order_by(Test.name)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_test_by_id(db: AsyncSession, test_id: str) -> Optional[Test]:
        query = (
            select(Test)
            .options(
                selectinload(Test.category),
                selectinload(Test.parameters).selectinload(TestParameter.reference_ranges)
            )
            .where(Test.id == test_id)
        )
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create_test(
        db: AsyncSession,
        test_in: TestCreate,
        creator_id: Optional[str] = None
    ) -> Test:
        existing = await db.execute(select(Test).where(Test.test_code == test_in.test_code.upper()))
        if existing.scalars().first():
            raise ConflictException(f"Test code '{test_in.test_code}' already exists.")

        test = Test(
            id=str(uuid.uuid4()),
            category_id=test_in.category_id,
            test_code=test_in.test_code.upper().strip(),
            name=test_in.name.strip(),
            short_name=test_in.short_name,
            description=test_in.description,
            specimen_type=test_in.specimen_type,
            container_type=test_in.container_type,
            price=test_in.price,
            turnaround_time_hours=test_in.turnaround_time_hours,
            is_active=test_in.is_active
        )
        db.add(test)
        await db.flush()

        # Add parameters and reference ranges if supplied
        if test_in.parameters:
            for p_in in test_in.parameters:
                param = TestParameter(
                    id=str(uuid.uuid4()),
                    test_id=test.id,
                    parameter_code=p_in.parameter_code.upper().strip(),
                    name=p_in.name.strip(),
                    unit=p_in.unit,
                    data_type=p_in.data_type,
                    display_order=p_in.display_order,
                    formula_expression=p_in.formula_expression,
                    is_active=p_in.is_active
                )
                db.add(param)
                await db.flush()

                if p_in.reference_ranges:
                    for r_in in p_in.reference_ranges:
                        ref_range = ReferenceRange(
                            id=str(uuid.uuid4()),
                            parameter_id=param.id,
                            gender=r_in.gender,
                            age_min_days=r_in.age_min_days,
                            age_max_days=r_in.age_max_days,
                            normal_min=r_in.normal_min,
                            normal_max=r_in.normal_max,
                            critical_low=r_in.critical_low,
                            critical_high=r_in.critical_high,
                            qualitative_normal=r_in.qualitative_normal,
                            interpretation_text=r_in.interpretation_text
                        )
                        db.add(ref_range)

        if creator_id:
            audit = AuditLog(
                id=str(uuid.uuid4()),
                user_id=creator_id,
                action=AuditActionEnum.CREATE_TEST,
                entity_name="Test",
                entity_id=test.id,
                details=f"Created clinical test {test.name} ({test.test_code})"
            )
            db.add(audit)

        await db.commit()
        return await CatalogService.get_test_by_id(db, test.id)

    @staticmethod
    async def update_test(
        db: AsyncSession,
        test_id: str,
        test_in: TestUpdate,
        actor_id: Optional[str] = None
    ) -> Test:
        test = await CatalogService.get_test_by_id(db, test_id)
        if not test:
            raise NotFoundException("Test", test_id)

        update_data = test_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(test, key, value)

        await db.commit()
        return await CatalogService.get_test_by_id(db, test_id)
