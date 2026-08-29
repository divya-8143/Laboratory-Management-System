import enum
from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, Date, Enum, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base


class GenderEnum(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class BloodGroupEnum(str, enum.Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    UNKNOWN = "UNKNOWN"


class Patient(Base):
    __tablename__ = "patients"

    id = Column(String(36), primary_key=True, index=True)
    patient_code = Column(String(50), unique=True, index=True, nullable=False)  # e.g., PAT-2026-0001
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, unique=True)  # Optional linked portal user
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    blood_group = Column(Enum(BloodGroupEnum), default=BloodGroupEnum.UNKNOWN, nullable=False)
    phone = Column(String(50), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(50), nullable=True)
    medical_history_notes = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user_account = relationship("User", back_populates="patient_profile")
    orders = relationship("Order", back_populates="patient", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def age_years(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    @property
    def age_in_days(self) -> int:
        return (date.today() - self.date_of_birth).days
