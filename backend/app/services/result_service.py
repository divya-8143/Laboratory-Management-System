import uuid
from datetime import datetime
from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc
from sqlalchemy.orm import selectinload

from app.models.result import TestResult, ResultFlagEnum
from app.models.order import Order, OrderItem, OrderStatusEnum
from app.models.sample import Sample, SampleStatusEnum
from app.models.patient import Patient
from app.models.catalog import Test, TestParameter, ReferenceRange, ParameterDataTypeEnum
from app.models.audit import AuditLog, AuditActionEnum
from app.schemas.result import BatchResultEntryRequest, WorklistItemResponse
from app.services.reference_range_evaluator import ReferenceRangeEvaluator
from app.core.exceptions import NotFoundException, ClinicalValidationError


class ResultService:
    @staticmethod
    async def get_technician_worklist(
        db: AsyncSession,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[WorklistItemResponse]:
        """
        Fetches all order items ready for laboratory testing or currently in progress.
        """
        query = (
            select(OrderItem)
            .join(Order)
            .join(Patient)
            .join(Test)
            .join(Sample)
            .options(
                selectinload(OrderItem.order).selectinload(Order.patient),
                selectinload(OrderItem.test).selectinload(Test.parameters),
                selectinload(OrderItem.sample),
                selectinload(OrderItem.results)
            )
            .where(
                Sample.status.in_([
                    SampleStatusEnum.RECEIVED_IN_LAB,
                    SampleStatusEnum.PROCESSING,
                    SampleStatusEnum.COLLECTED
                ])
            )
        )

        if status:
            query = query.where(OrderItem.status == status)

        if search:
            pattern = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Order.order_number.ilike(pattern),
                    Sample.barcode.ilike(pattern),
                    Patient.first_name.ilike(pattern),
                    Patient.last_name.ilike(pattern),
                    Patient.patient_code.ilike(pattern),
                    Test.name.ilike(pattern),
                    Test.test_code.ilike(pattern)
                )
            )

        query = query.order_by(
            Order.priority.desc(),  # STAT / URGENT first
            Order.created_at.asc()
        )

        res = await db.execute(query)
        order_items = list(res.scalars().all())

        worklist = []
        for item in order_items:
            patient = item.order.patient
            worklist.append(
                WorklistItemResponse(
                    order_item_id=item.id,
                    order_id=item.order.id,
                    order_number=item.order.order_number,
                    priority=item.order.priority.value,
                    patient_id=patient.id,
                    patient_name=patient.full_name,
                    patient_code=patient.patient_code,
                    patient_gender=patient.gender.value,
                    patient_age=patient.age_years,
                    test_id=item.test.id,
                    test_code=item.test.test_code,
                    test_name=item.test.name,
                    sample_barcode=item.sample.barcode if item.sample else "N/A",
                    sample_status=item.sample.status.value if item.sample else "N/A",
                    item_status=item.status,
                    results_count=len(item.results),
                    parameters_count=len(item.test.parameters)
                )
            )
        return worklist

    @staticmethod
    async def enter_batch_results(
        db: AsyncSession,
        batch_in: BatchResultEntryRequest,
        technician_id: str
    ) -> List[TestResult]:
        """
        Record parameter results, automatically evaluate against patient-specific
        reference ranges, and calculate abnormal/critical clinical flags.
        """
        # Fetch OrderItem with deep relations
        query = (
            select(OrderItem)
            .options(
                selectinload(OrderItem.order).selectinload(Order.patient),
                selectinload(OrderItem.test).selectinload(Test.parameters).selectinload(TestParameter.reference_ranges),
                selectinload(OrderItem.sample),
                selectinload(OrderItem.results)
            )
            .where(OrderItem.id == batch_in.order_item_id)
        )
        res = await db.execute(query)
        item = res.scalars().first()
        if not item:
            raise NotFoundException("OrderItem", batch_in.order_item_id)

        patient = item.order.patient
        patient_gender = patient.gender.value
        patient_age_days = patient.age_in_days

        # Build map of test parameters
        param_map = {p.id: p for p in item.test.parameters}

        # Clear or update existing results for this order item
        existing_results_map = {r.parameter_id: r for r in item.results}

        saved_results = []
        has_abnormal = False
        has_critical = False

        for entry in batch_in.results:
            param = param_map.get(entry.parameter_id)
            if not param:
                continue

            # Find matching reference range for patient's age and gender
            matching_range = ReferenceRangeEvaluator.find_matching_range(
                param.reference_ranges,
                patient_gender=patient_gender,
                patient_age_days=patient_age_days
            )

            # Evaluate clinical bounds
            flag, range_display, is_abnormal, is_critical = ReferenceRangeEvaluator.evaluate_result(
                data_type=param.data_type,
                numeric_val=entry.numeric_value,
                text_val=entry.text_value,
                ref_range=matching_range
            )

            if is_abnormal:
                has_abnormal = True
            if is_critical:
                has_critical = True

            formatted_val = (
                f"{entry.numeric_value:.2f}".rstrip("0").rstrip(".")
                if entry.numeric_value is not None
                else (entry.text_value or "")
            )

            existing_res = existing_results_map.get(param.id)
            if existing_res:
                existing_res.numeric_value = entry.numeric_value
                existing_res.text_value = entry.text_value
                existing_res.formatted_value = formatted_val
                existing_res.flag = flag
                existing_res.reference_range_display = range_display
                existing_res.is_abnormal = is_abnormal
                existing_res.is_critical = is_critical
                existing_res.technician_notes = entry.technician_notes
                existing_res.entered_by_id = technician_id
                existing_res.updated_at = datetime.utcnow()
                saved_results.append(existing_res)
            else:
                new_result = TestResult(
                    id=str(uuid.uuid4()),
                    order_item_id=item.id,
                    parameter_id=param.id,
                    sample_id=item.sample_id,
                    numeric_value=entry.numeric_value,
                    text_value=entry.text_value,
                    formatted_value=formatted_val,
                    flag=flag,
                    reference_range_display=range_display,
                    is_abnormal=is_abnormal,
                    is_critical=is_critical,
                    technician_notes=entry.technician_notes,
                    entered_by_id=technician_id,
                    entered_at=datetime.utcnow()
                )
                db.add(new_result)
                saved_results.append(new_result)

        # Mark item as RESULTED / PROCESSING
        item.status = "RESULTED"
        if item.sample:
            item.sample.status = SampleStatusEnum.PROCESSING

        # Audit
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=technician_id,
            action=AuditActionEnum.ENTER_RESULTS,
            entity_name="OrderItem",
            entity_id=item.id,
            details=f"Entered {len(saved_results)} results for test {item.test.name} on order {item.order.order_number}. Abnormal: {has_abnormal}, Critical: {has_critical}"
        )
        db.add(audit)

        await db.commit()

        # Re-fetch populated results
        res_query = (
            select(TestResult)
            .options(
                selectinload(TestResult.parameter),
                selectinload(TestResult.technician)
            )
            .where(TestResult.order_item_id == item.id)
        )
        out = await db.execute(res_query)
        return list(out.scalars().all())

    @staticmethod
    async def get_results_for_order(db: AsyncSession, order_id: str) -> List[TestResult]:
        query = (
            select(TestResult)
            .join(OrderItem)
            .options(
                selectinload(TestResult.parameter),
                selectinload(TestResult.technician)
            )
            .where(OrderItem.order_id == order_id)
        )
        res = await db.execute(query)
        return list(res.scalars().all())
