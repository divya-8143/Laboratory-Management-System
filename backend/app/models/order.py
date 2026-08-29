import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Text, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class OrderPriorityEnum(str, enum.Enum):
    ROUTINE = "ROUTINE"
    URGENT = "URGENT"
    STAT = "STAT"  # Critical immediate processing


class OrderStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    SAMPLE_COLLECTED = "SAMPLE_COLLECTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)  # e.g., "ORD-2026-0001"
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    referring_doctor = Column(String(150), nullable=True)
    clinical_notes = Column(Text, nullable=True)
    priority = Column(Enum(OrderPriorityEnum), default=OrderPriorityEnum.ROUTINE, nullable=False)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING, nullable=False, index=True)
    
    # Financial summary cached on order
    subtotal = Column(Float, default=0.0, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)

    created_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="orders")
    creator = relationship("User", foreign_keys=[created_by_id], back_populates="orders_created")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    samples = relationship("Sample", back_populates="order", cascade="all, delete-orphan")
    invoice = relationship("Invoice", back_populates="order", uselist=False, cascade="all, delete-orphan")
    lab_report = relationship("LabReport", back_populates="order", uselist=False, cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String(36), primary_key=True, index=True)
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False, index=True)
    test_id = Column(String(36), ForeignKey("tests.id"), nullable=False, index=True)
    sample_id = Column(String(36), ForeignKey("samples.id"), nullable=True, index=True)
    price = Column(Float, nullable=False)
    status = Column(String(50), default="PENDING", nullable=False)  # PENDING, PROCESSING, COMPLETED, CANCELLED

    # Relationships
    order = relationship("Order", back_populates="order_items")
    test = relationship("Test", back_populates="order_items")
    sample = relationship("Sample", back_populates="order_items")
    results = relationship("TestResult", back_populates="order_item", cascade="all, delete-orphan")
