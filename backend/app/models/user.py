import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class RoleType(str, enum.Enum):
    ADMIN = "ADMIN"
    RECEPTIONIST = "RECEPTIONIST"
    TECHNICIAN = "TECHNICIAN"
    DOCTOR = "DOCTOR"
    PATIENT = "PATIENT"


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum(RoleType), nullable=False, default=RoleType.PATIENT, index=True)
    phone = Column(String(50), nullable=True)
    department = Column(String(100), nullable=True)
    license_number = Column(String(100), nullable=True)  # Doctor / Technician medical license
    signature_image_url = Column(Text, nullable=True)  # Base64 or URL of digital signature
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    orders_created = relationship("Order", foreign_keys="Order.created_by_id", back_populates="creator")
    samples_collected = relationship("Sample", foreign_keys="Sample.collected_by_id", back_populates="collector")
    results_entered = relationship("TestResult", foreign_keys="TestResult.entered_by_id", back_populates="technician")
    reports_verified = relationship("LabReport", foreign_keys="LabReport.verified_by_doctor_id", back_populates="verified_by_doctor")
    audit_logs = relationship("AuditLog", back_populates="user")
    patient_profile = relationship("Patient", back_populates="user_account", uselist=False)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
