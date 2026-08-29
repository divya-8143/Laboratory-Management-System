import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ReportStatusEnum(str, enum.Enum):
    DRAFT = "DRAFT"
    VERIFIED = "VERIFIED"
    PUBLISHED = "PUBLISHED"
    AMENDED = "AMENDED"


class LabReport(Base):
    __tablename__ = "lab_reports"

    id = Column(String(36), primary_key=True, index=True)
    order_id = Column(String(36), ForeignKey("orders.id"), unique=True, nullable=False, index=True)
    report_number = Column(String(50), unique=True, index=True, nullable=False)  # e.g., "REP-2026-0001"
    status = Column(Enum(ReportStatusEnum), default=ReportStatusEnum.DRAFT, nullable=False, index=True)
    
    verified_by_doctor_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    
    pathologist_comments = Column(Text, nullable=True)
    clinical_interpretation = Column(Text, nullable=True)
    pdf_filename = Column(String(255), nullable=True)
    pdf_path = Column(Text, nullable=True)
    verification_qr_hash = Column(String(100), unique=True, index=True, nullable=False)
    
    download_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="lab_report")
    verified_by_doctor = relationship("User", foreign_keys=[verified_by_doctor_id], back_populates="reports_verified")
