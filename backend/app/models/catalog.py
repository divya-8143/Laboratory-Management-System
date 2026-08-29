import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Text, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class SpecimenTypeEnum(str, enum.Enum):
    WHOLE_BLOOD = "WHOLE_BLOOD"
    SERUM = "SERUM"
    PLASMA = "PLASMA"
    URINE = "URINE"
    CSF = "CSF"
    STOOL = "STOOL"
    SPUTUM = "SPUTUM"
    SWAB = "SWAB"
    SYNOVIAL_FLUID = "SYNOVIAL_FLUID"


class ContainerTypeEnum(str, enum.Enum):
    EDTA_LAVENDER = "EDTA_LAVENDER"
    SST_GOLD_YELLOW = "SST_GOLD_YELLOW"
    PLAIN_RED = "PLAIN_RED"
    SODIUM_CITRATE_BLUE = "SODIUM_CITRATE_BLUE"
    SODIUM_FLUORIDE_GREY = "SODIUM_FLUORIDE_GREY"
    HEPARIN_GREEN = "HEPARIN_GREEN"
    STERILE_CONTAINER = "STERILE_CONTAINER"


class ParameterDataTypeEnum(str, enum.Enum):
    NUMERIC = "NUMERIC"
    TEXT = "TEXT"
    QUALITATIVE = "QUALITATIVE"  # Positive/Negative/Reactive
    CALCULATED = "CALCULATED"    # Auto-calculated from other parameters


class TestCategory(Base):
    __tablename__ = "test_categories"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, nullable=False)

    tests = relationship("Test", back_populates="category", cascade="all, delete-orphan")


class Test(Base):
    __tablename__ = "tests"

    id = Column(String(36), primary_key=True, index=True)
    category_id = Column(String(36), ForeignKey("test_categories.id"), nullable=False)
    test_code = Column(String(50), unique=True, index=True, nullable=False)  # e.g., "CBC", "LFT"
    name = Column(String(150), nullable=False, index=True)
    short_name = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    specimen_type = Column(Enum(SpecimenTypeEnum), nullable=False)
    container_type = Column(Enum(ContainerTypeEnum), nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    turnaround_time_hours = Column(Integer, default=24)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    category = relationship("TestCategory", back_populates="tests")
    parameters = relationship("TestParameter", back_populates="test", cascade="all, delete-orphan", order_by="TestParameter.display_order")
    order_items = relationship("OrderItem", back_populates="test")


class TestParameter(Base):
    __tablename__ = "test_parameters"

    id = Column(String(36), primary_key=True, index=True)
    test_id = Column(String(36), ForeignKey("tests.id"), nullable=False)
    parameter_code = Column(String(50), nullable=False)  # e.g., "HGB", "WBC", "PLT"
    name = Column(String(150), nullable=False)
    unit = Column(String(50), nullable=True)  # e.g., "g/dL", "10^3/uL", "mg/dL"
    data_type = Column(Enum(ParameterDataTypeEnum), default=ParameterDataTypeEnum.NUMERIC, nullable=False)
    display_order = Column(Integer, default=0)
    formula_expression = Column(String(255), nullable=True)  # e.g., for calculating ratios or eGFR
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    test = relationship("Test", back_populates="parameters")
    reference_ranges = relationship("ReferenceRange", back_populates="parameter", cascade="all, delete-orphan")
    results = relationship("TestResult", back_populates="parameter")


class ReferenceRange(Base):
    __tablename__ = "reference_ranges"

    id = Column(String(36), primary_key=True, index=True)
    parameter_id = Column(String(36), ForeignKey("test_parameters.id"), nullable=False)
    gender = Column(String(20), default="BOTH", nullable=False)  # "MALE", "FEMALE", "BOTH"
    age_min_days = Column(Integer, default=0, nullable=False)     # Minimum age in days
    age_max_days = Column(Integer, default=43800, nullable=False) # Maximum age in days (120 years)
    normal_min = Column(Float, nullable=True)
    normal_max = Column(Float, nullable=True)
    critical_low = Column(Float, nullable=True)
    critical_high = Column(Float, nullable=True)
    qualitative_normal = Column(String(100), nullable=True)  # e.g., "Negative", "Non-Reactive"
    interpretation_text = Column(Text, nullable=True)

    # Relationships
    parameter = relationship("TestParameter", back_populates="reference_ranges")
