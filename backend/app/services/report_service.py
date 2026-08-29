import uuid
import os
from datetime import datetime
from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc
from sqlalchemy.orm import selectinload

from app.models.report import LabReport, ReportStatusEnum
from app.models.order import Order, OrderStatusEnum, OrderItem
from app.models.sample import Sample
from app.models.patient import Patient
from app.models.user import User
from app.models.catalog import Test, TestParameter
from app.models.result import TestResult
from app.models.audit import AuditLog, AuditActionEnum
from app.schemas.report import ReportVerificationRequest, ReportVerificationPublicInfo
from app.services.report_generator import ReportGeneratorService
from app.core.config import settings
from app.core.exceptions import NotFoundException, ClinicalValidationError


class ReportService:
    @staticmethod
    async def get_report_by_id(db: AsyncSession, report_id: str) -> Optional[LabReport]:
        query = (
            select(LabReport)
            .options(
                selectinload(LabReport.verified_by_doctor),
                selectinload(LabReport.order).selectinload(Order.patient),
                selectinload(LabReport.order).selectinload(Order.order_items).selectinload(OrderItem.test),
                selectinload(LabReport.order).selectinload(Order.order_items).selectinload(OrderItem.results).selectinload(TestResult.parameter)
            )
            .where(LabReport.id == report_id)
        )
        res = await db.execute(query)
        return res.scalars().first()

    @staticmethod
    async def get_report_by_order_id(db: AsyncSession, order_id: str) -> Optional[LabReport]:
        query = (
            select(LabReport)
            .options(
                selectinload(LabReport.verified_by_doctor),
                selectinload(LabReport.order).selectinload(Order.patient),
                selectinload(LabReport.order).selectinload(Order.order_items).selectinload(OrderItem.test),
                selectinload(LabReport.order).selectinload(Order.order_items).selectinload(OrderItem.results).selectinload(TestResult.parameter)
            )
            .where(LabReport.order_id == order_id)
        )
        res = await db.execute(query)
        return res.scalars().first()

    @staticmethod
    async def list_reports(
        db: AsyncSession,
        status: Optional[ReportStatusEnum] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[LabReport]:
        query = (
            select(LabReport)
            .join(Order)
            .join(Patient)
            .options(
                selectinload(LabReport.verified_by_doctor),
                selectinload(LabReport.order).selectinload(Order.patient),
                selectinload(LabReport.order).selectinload(Order.order_items).selectinload(OrderItem.test)
            )
        )
        if status:
            query = query.where(LabReport.status == status)
        if search:
            pattern = f"%{search.strip()}%"
            query = query.where(
                or_(
                    LabReport.report_number.ilike(pattern),
                    Order.order_number.ilike(pattern),
                    Patient.first_name.ilike(pattern),
                    Patient.last_name.ilike(pattern),
                    Patient.patient_code.ilike(pattern)
                )
            )

        query = query.order_by(desc(LabReport.created_at)).offset(skip).limit(limit)
        res = await db.execute(query)
        return list(res.scalars().all())

    @staticmethod
    async def verify_and_publish_report(
        db: AsyncSession,
        report_id: str,
        verify_in: ReportVerificationRequest,
        doctor_id: str
    ) -> LabReport:
        report = await ReportService.get_report_by_id(db, report_id)
        if not report:
            raise NotFoundException("Report", report_id)

        doctor_res = await db.execute(select(User).where(User.id == doctor_id))
        doctor = doctor_res.scalars().first()

        order = report.order
        patient = order.patient

        # Verify results exist
        has_results = False
        for item in order.order_items:
            if item.results:
                has_results = True
                item.status = "COMPLETED"
        if not has_results:
            raise ClinicalValidationError("Cannot verify report with no entered laboratory test results.")

        # Update report
        report.status = ReportStatusEnum.VERIFIED
        report.verified_by_doctor_id = doctor_id
        report.verified_at = datetime.utcnow()
        report.pathologist_comments = verify_in.pathologist_comments
        report.clinical_interpretation = verify_in.clinical_interpretation

        # Generate & save PDF
        pdf_path = ReportGeneratorService.generate_pdf_report(
            report=report,
            order=order,
            patient=patient,
            doctor=doctor
        )
        report.pdf_filename = os.path.basename(pdf_path)
        report.pdf_path = pdf_path

        # Update order status to COMPLETED
        order.status = OrderStatusEnum.COMPLETED

        # Audit
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=doctor_id,
            action=AuditActionEnum.VERIFY_REPORT,
            entity_name="LabReport",
            entity_id=report.id,
            details=f"Dr. {doctor.full_name if doctor else ''} verified and published laboratory report {report.report_number}"
        )
        db.add(audit)

        await db.commit()
        return await ReportService.get_report_by_id(db, report.id)

    @staticmethod
    async def verify_public_qr_hash(db: AsyncSession, qr_hash: str) -> ReportVerificationPublicInfo:
        query = (
            select(LabReport)
            .options(
                selectinload(LabReport.verified_by_doctor),
                selectinload(LabReport.order).selectinload(Order.patient),
                selectinload(LabReport.order).selectinload(Order.order_items).selectinload(OrderItem.test)
            )
            .where(LabReport.verification_qr_hash == qr_hash.strip())
        )
        res = await db.execute(query)
        report = res.scalars().first()
        if not report:
            raise NotFoundException("Verification QR hash", qr_hash)

        patient = report.order.patient
        initials = f"{patient.first_name[0]}.{patient.last_name[0]}." if patient.first_name and patient.last_name else "P.N."
        tests = [item.test.name for item in report.order.order_items]

        return ReportVerificationPublicInfo(
            report_number=report.report_number,
            status=report.status.value,
            verified_at=report.verified_at,
            verified_by=f"Dr. {report.verified_by_doctor.full_name}" if report.verified_by_doctor else None,
            patient_initials=initials,
            patient_code=patient.patient_code,
            order_number=report.order.order_number,
            tests_included=tests,
            is_authentic=True,
            laboratory_name=settings.LAB_NAME
        )
