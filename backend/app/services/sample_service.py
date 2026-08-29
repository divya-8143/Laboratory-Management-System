import uuid
from datetime import datetime
from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc
from sqlalchemy.orm import selectinload

from app.models.sample import Sample, SampleStatusHistory, SampleStatusEnum
from app.models.order import Order, OrderStatusEnum, OrderItem
from app.models.patient import Patient
from app.models.audit import AuditLog, AuditActionEnum
from app.schemas.sample import SampleBarcodeInfo
from app.core.exceptions import NotFoundException, ClinicalValidationError


class SampleService:
    @staticmethod
    async def get_sample_by_id(db: AsyncSession, sample_id: str) -> Optional[Sample]:
        query = (
            select(Sample)
            .options(
                selectinload(Sample.order).selectinload(Order.patient),
                selectinload(Sample.collector),
                selectinload(Sample.status_history).selectinload(SampleStatusHistory.changed_by),
                selectinload(Sample.order_items).selectinload(OrderItem.test)
            )
            .where(Sample.id == sample_id)
        )
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_sample_by_barcode(db: AsyncSession, barcode: str) -> Optional[Sample]:
        query = (
            select(Sample)
            .options(
                selectinload(Sample.order).selectinload(Order.patient),
                selectinload(Sample.collector),
                selectinload(Sample.status_history).selectinload(SampleStatusHistory.changed_by),
                selectinload(Sample.order_items).selectinload(OrderItem.test)
            )
            .where(Sample.barcode == barcode.strip())
        )
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def list_samples_queue(
        db: AsyncSession,
        status: Optional[SampleStatusEnum] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Sample]:
        query = (
            select(Sample)
            .options(
                selectinload(Sample.order).selectinload(Order.patient),
                selectinload(Sample.collector),
                selectinload(Sample.status_history).selectinload(SampleStatusHistory.changed_by),
                selectinload(Sample.order_items).selectinload(OrderItem.test)
            )
        )
        if status:
            query = query.where(Sample.status == status)
        if search:
            pattern = f"%{search.strip()}%"
            query = query.join(Order).join(Patient).where(
                or_(
                    Sample.barcode.ilike(pattern),
                    Order.order_number.ilike(pattern),
                    Patient.first_name.ilike(pattern),
                    Patient.last_name.ilike(pattern),
                    Patient.patient_code.ilike(pattern)
                )
            )

        query = query.order_by(desc(Sample.created_at)).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def mark_sample_collected(
        db: AsyncSession,
        sample_id: str,
        collector_id: str,
        notes: Optional[str] = None
    ) -> Sample:
        sample = await SampleService.get_sample_by_id(db, sample_id)
        if not sample:
            raise NotFoundException("Sample", sample_id)

        if sample.status not in [SampleStatusEnum.PENDING_COLLECTION, SampleStatusEnum.REJECTED]:
            raise ClinicalValidationError(f"Sample is already in status '{sample.status.value}'.")

        old_status = sample.status.value
        sample.status = SampleStatusEnum.COLLECTED
        sample.collected_at = datetime.utcnow()
        sample.collected_by_id = collector_id
        if notes:
            sample.notes = f"{sample.notes or ''}\n{notes}".strip()

        # Add History
        history = SampleStatusHistory(
            id=str(uuid.uuid4()),
            sample_id=sample.id,
            from_status=old_status,
            to_status=SampleStatusEnum.COLLECTED.value,
            changed_by_id=collector_id,
            comments=notes or "Specimen collected by phlebotomist."
        )
        db.add(history)

        # Update order item statuses
        for item in sample.order_items:
            if item.status == "PENDING":
                item.status = "SAMPLE_COLLECTED"

        # Update parent order status if pending
        if sample.order and sample.order.status == OrderStatusEnum.PENDING:
            sample.order.status = OrderStatusEnum.SAMPLE_COLLECTED

        # Audit
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=collector_id,
            action=AuditActionEnum.COLLECT_SAMPLE,
            entity_name="Sample",
            entity_id=sample.id,
            details=f"Collected specimen tube {sample.barcode} ({sample.container_type.value})"
        )
        db.add(audit)

        await db.commit()
        return await SampleService.get_sample_by_id(db, sample.id)

    @staticmethod
    async def mark_sample_received(
        db: AsyncSession,
        sample_id: str,
        technician_id: str
    ) -> Sample:
        sample = await SampleService.get_sample_by_id(db, sample_id)
        if not sample:
            raise NotFoundException("Sample", sample_id)

        if sample.status != SampleStatusEnum.COLLECTED:
            raise ClinicalValidationError("Specimen must be COLLECTED before it can be received in the laboratory.")

        old_status = sample.status.value
        sample.status = SampleStatusEnum.RECEIVED_IN_LAB
        sample.received_at = datetime.utcnow()
        sample.received_by_id = technician_id

        history = SampleStatusHistory(
            id=str(uuid.uuid4()),
            sample_id=sample.id,
            from_status=old_status,
            to_status=SampleStatusEnum.RECEIVED_IN_LAB.value,
            changed_by_id=technician_id,
            comments="Specimen accessioned & received in testing laboratory."
        )
        db.add(history)

        # Update order status to IN_PROGRESS
        if sample.order:
            sample.order.status = OrderStatusEnum.IN_PROGRESS

        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=technician_id,
            action=AuditActionEnum.RECEIVE_SAMPLE,
            entity_name="Sample",
            entity_id=sample.id,
            details=f"Received sample tube {sample.barcode} in laboratory worklist"
        )
        db.add(audit)

        await db.commit()
        return await SampleService.get_sample_by_id(db, sample.id)

    @staticmethod
    async def reject_sample(
        db: AsyncSession,
        sample_id: str,
        reason: str,
        actor_id: str
    ) -> Sample:
        sample = await SampleService.get_sample_by_id(db, sample_id)
        if not sample:
            raise NotFoundException("Sample", sample_id)

        old_status = sample.status.value
        sample.status = SampleStatusEnum.REJECTED
        sample.rejection_reason = reason.strip()

        history = SampleStatusHistory(
            id=str(uuid.uuid4()),
            sample_id=sample.id,
            from_status=old_status,
            to_status=SampleStatusEnum.REJECTED.value,
            changed_by_id=actor_id,
            comments=f"SPECIMEN REJECTED: {reason}"
        )
        db.add(history)

        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=actor_id,
            action=AuditActionEnum.REJECT_SAMPLE,
            entity_name="Sample",
            entity_id=sample.id,
            details=f"Rejected sample {sample.barcode}. Reason: {reason}"
        )
        db.add(audit)

        await db.commit()
        return await SampleService.get_sample_by_id(db, sample.id)
