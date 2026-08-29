import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ResultFlagEnum(str, enum.Enum):
    NORMAL = "NORMAL"
    LOW = "LOW"
    HIGH = "HIGH"
    CRITICAL_LOW = "CRITICAL_LOW"
    CRITICAL_HIGH = "CRITICAL_HIGH"
    ABNORMAL = "ABNORMAL"  # For qualitative findings (e.g. Reactive)


class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(String(36), primary_key=True, index=True)
    order_item_id = Column(String(36), ForeignKey("order_items.id"), nullable=False, index=True)
    parameter_id = Column(String(36), ForeignKey("test_parameters.id"), nullable=False, index=True)
    sample_id = Column(String(36), ForeignKey("samples.id"), nullable=False, index=True)
    
    numeric_value = Column(Float, nullable=True)
    text_value = Column(String(255), nullable=True)
    formatted_value = Column(String(255), nullable=False)  # Display representation e.g. "13.5", "Negative"
    
    flag = Column(Enum(ResultFlagEnum), default=ResultFlagEnum.NORMAL, nullable=False, index=True)
    reference_range_display = Column(String(255), nullable=True)  # Snapshot of normal range at time of testing
    is_abnormal = Column(Boolean, default=False, nullable=False)
    is_critical = Column(Boolean, default=False, nullable=False)
    
    technician_notes = Column(Text, nullable=True)
    entered_by_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    entered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    order_item = relationship("OrderItem", back_populates="results")
    parameter = relationship("TestParameter", back_populates="results")
    sample = relationship("Sample", back_populates="results")
    technician = relationship("User", foreign_keys=[entered_by_id], back_populates="results_entered")
