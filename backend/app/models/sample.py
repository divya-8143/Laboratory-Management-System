import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.catalog import SpecimenTypeEnum, ContainerTypeEnum


class SampleStatusEnum(str, enum.Enum):
    PENDING_COLLECTION = "PENDING_COLLECTION"
    COLLECTED = "COLLECTED"
    RECEIVED_IN_LAB = "RECEIVED_IN_LAB"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


class Sample(Base):
    __tablename__ = "samples"

    id = Column(String(36), primary_key=True, index=True)
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False, index=True)
    barcode = Column(String(50), unique=True, index=True, nullable=False)  # e.g., "SMP-984729184"
    specimen_type = Column(Enum(SpecimenTypeEnum), nullable=False)
    container_type = Column(Enum(ContainerTypeEnum), nullable=False)
    status = Column(Enum(SampleStatusEnum), default=SampleStatusEnum.PENDING_COLLECTION, nullable=False, index=True)
    
    collected_at = Column(DateTime, nullable=True)
    collected_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    received_at = Column(DateTime, nullable=True)
    received_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    rejection_reason = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="samples")
    collector = relationship("User", foreign_keys=[collected_by_id], back_populates="samples_collected")
    receiver = relationship("User", foreign_keys=[received_by_id])
    order_items = relationship("OrderItem", back_populates="sample")
    results = relationship("TestResult", back_populates="sample")
    status_history = relationship("SampleStatusHistory", back_populates="sample", cascade="all, delete-orphan", order_by="SampleStatusHistory.timestamp.desc()")


class SampleStatusHistory(Base):
    __tablename__ = "sample_status_history"

    id = Column(String(36), primary_key=True, index=True)
    sample_id = Column(String(36), ForeignKey("samples.id"), nullable=False, index=True)
    from_status = Column(String(50), nullable=True)
    to_status = Column(String(50), nullable=False)
    changed_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    comments = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    sample = relationship("Sample", back_populates="status_history")
    changed_by = relationship("User")
