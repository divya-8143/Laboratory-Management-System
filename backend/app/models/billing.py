import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class PaymentStatusEnum(str, enum.Enum):
    UNPAID = "UNPAID"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    REFUNDED = "REFUNDED"


class PaymentMethodEnum(str, enum.Enum):
    CASH = "CASH"
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    UPI = "UPI"
    BANK_TRANSFER = "BANK_TRANSFER"
    INSURANCE = "INSURANCE"


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String(36), primary_key=True, index=True)
    order_id = Column(String(36), ForeignKey("orders.id"), unique=True, nullable=False, index=True)
    invoice_number = Column(String(50), unique=True, index=True, nullable=False)  # e.g., "INV-2026-0001"
    
    subtotal = Column(Float, nullable=False, default=0.0)
    discount_amount = Column(Float, nullable=False, default=0.0)
    tax_amount = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False, default=0.0)
    paid_amount = Column(Float, nullable=False, default=0.0)
    balance_amount = Column(Float, nullable=False, default=0.0)
    
    payment_status = Column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.UNPAID, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="invoice")
    payments = relationship("Payment", back_populates="invoice", cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String(36), primary_key=True, index=True)
    invoice_id = Column(String(36), ForeignKey("invoices.id"), nullable=False, index=True)
    payment_reference = Column(String(100), unique=True, index=True, nullable=False)  # e.g., "PAY-2026-0001"
    amount = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethodEnum), default=PaymentMethodEnum.CASH, nullable=False)
    transaction_id = Column(String(100), nullable=True)
    received_by_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    paid_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    invoice = relationship("Invoice", back_populates="payments")
    received_by = relationship("User")
