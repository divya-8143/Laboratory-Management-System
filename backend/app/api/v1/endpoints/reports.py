import os
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, Response
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_roles, RoleEnum, get_current_user_payload
from app.models.report import ReportStatusEnum
from app.models.audit import AuditLog, AuditActionEnum
from app.schemas.report import (
    ReportResponse,
    ReportVerificationRequest,
    ReportVerificationPublicInfo
)
from app.services.report_service import ReportService
from app.core.exceptions import NotFoundException

router = APIRouter(prefix="/reports", tags=["Reports & Medical Sign-off"])


@router.get("", response_model=List[ReportResponse])
async def list_reports(
    status: Optional[ReportStatusEnum] = Query(None),
    search: Optional[str] = Query(None, description="Search by report number, patient, or order"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_db)
):
    """List lab reports with verification status filters."""
    return await ReportService.list_reports(db, status=status, search=search, skip=skip, limit=limit)


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report_by_id(
    report_id: str,
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_db)
):
    """Get report details and clinical verification metadata."""
    report = await ReportService.get_report_by_id(db, report_id)
    if not report:
        raise NotFoundException("Report", report_id)
    return report


@router.get("/order/{order_id}", response_model=ReportResponse)
async def get_report_by_order_id(
    order_id: str,
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve report for a specific order."""
    report = await ReportService.get_report_by_order_id(db, order_id)
    if not report:
        raise NotFoundException("Report for order", order_id)
    return report


@router.post("/{report_id}/verify", response_model=ReportResponse)
async def verify_report(
    report_id: str,
    verify_in: ReportVerificationRequest,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.DOCTOR])),
    db: AsyncSession = Depends(get_db)
):
    """Doctor / Pathologist digital sign-off and automated PDF generation."""
    return await ReportService.verify_and_publish_report(
        db, report_id, verify_in, doctor_id=payload["sub"]
    )


@router.get("/{report_id}/pdf")
async def download_report_pdf(
    report_id: str,
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_db)
):
    """Download official signed PDF laboratory report."""
    report = await ReportService.get_report_by_id(db, report_id)
    if not report:
        raise NotFoundException("Report", report_id)

    # Ensure PDF exists; if missing, generate on demand
    if not report.pdf_path or not os.path.exists(report.pdf_path):
        from app.services.report_generator import ReportGeneratorService
        pdf_path = ReportGeneratorService.generate_pdf_report(
            report=report,
            order=report.order,
            patient=report.order.patient,
            doctor=report.verified_by_doctor
        )
        report.pdf_path = pdf_path
        report.pdf_filename = os.path.basename(pdf_path)
        await db.commit()

    report.download_count += 1
    await db.commit()

    return FileResponse(
        path=report.pdf_path,
        media_type="application/pdf",
        filename=f"{report.report_number}.pdf"
    )


@router.get("/public/verify/{qr_hash}", response_model=ReportVerificationPublicInfo)
async def public_verify_report(qr_hash: str, db: AsyncSession = Depends(get_db)):
    """Public tamper-proof QR code verification endpoint for third-party validation."""
    return await ReportService.verify_public_qr_hash(db, qr_hash)
