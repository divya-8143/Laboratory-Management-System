import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class AuditActionEnum(str, enum.Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    CREATE_PATIENT = "CREATE_PATIENT"
    UPDATE_PATIENT = "UPDATE_PATIENT"
    CREATE_ORDER = "CREATE_ORDER"
    CANCEL_ORDER = "CANCEL_ORDER"
    COLLECT_SAMPLE = "COLLECT_SAMPLE"
    REJECT_SAMPLE = "REJECT_SAMPLE"
    RECEIVE_SAMPLE = "RECEIVE_SAMPLE"
    ENTER_RESULTS = "ENTER_RESULTS"
    UPDATE_RESULTS = "UPDATE_RESULTS"
    VERIFY_REPORT = "VERIFY_REPORT"
    DOWNLOAD_REPORT = "DOWNLOAD_REPORT"
    RECORD_PAYMENT = "RECORD_PAYMENT"
    CREATE_TEST = "CREATE_TEST"
    UPDATE_TEST = "UPDATE_TEST"


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    action = Column(Enum(AuditActionEnum), nullable=False, index=True)
    entity_name = Column(String(100), nullable=False, index=True)
    entity_id = Column(String(100), nullable=True, index=True)
    
    details = Column(Text, nullable=True)
    old_state = Column(JSON, nullable=True)
    new_state = Column(JSON, nullable=True)
    
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
