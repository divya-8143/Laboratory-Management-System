"""
AcuPath Enterprise LIS - Blood Bank & Transfusion Medicine Subsystem
Handles ABO/Rh blood typing, Indirect Antiglobulin Test (IAT) antibody screening,
cross-match compatibility verification, Packed Red Blood Cells (PRBC) unit allocation,
and Adverse Transfusion Reaction investigation workflows.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import datetime
import uuid


@dataclass
class BloodUnit:
    unit_din: str = "W1234 26 123456 00"  # ISBT-128 Donation Identification Number
    product_code: str = "E0123"           # Red Blood Cells Leukocytes Reduced
    blood_group: str = "O_POSITIVE"       # A_POS | A_NEG | B_POS | B_NEG | AB_POS | AB_NEG | O_POS | O_NEG
    volume_ml: int = 350
    anticoagulant: str = "CPDA-1"
    collection_date: datetime.date = field(default_factory=datetime.date.today)
    expiration_date: datetime.date = field(default_factory=lambda: datetime.date.today() + datetime.timedelta(days=42))
    storage_fridge: str = "BLOOD_BANK_FRIDGE_01 (4C)"
    crossmatched_patient_id: Optional[str] = None
    is_issued: bool = False


class TransfusionSafetyEngine:
    """Verifies recipient-donor immunological compatibility according to AABB standards."""

    COMPATIBILITY_MATRIX = {
        "O_NEGATIVE": ["O_NEGATIVE"],
        "O_POSITIVE": ["O_NEGATIVE", "O_POSITIVE"],
        "A_NEGATIVE": ["O_NEGATIVE", "A_NEGATIVE"],
        "A_POSITIVE": ["O_NEGATIVE", "O_POSITIVE", "A_NEGATIVE", "A_POSITIVE"],
        "B_NEGATIVE": ["O_NEGATIVE", "B_NEGATIVE"],
        "B_POSITIVE": ["O_NEGATIVE", "O_POSITIVE", "B_NEGATIVE", "B_POSITIVE"],
        "AB_NEGATIVE": ["O_NEGATIVE", "A_NEGATIVE", "B_NEGATIVE", "AB_NEGATIVE"],
        "AB_POSITIVE": ["O_NEGATIVE", "O_POSITIVE", "A_NEGATIVE", "A_POSITIVE", "B_NEGATIVE", "B_POSITIVE", "AB_NEGATIVE", "AB_POSITIVE"]
    }

    @classmethod
    def verify_compatibility(cls, recipient_type: str, donor_unit_type: str) -> bool:
        valid_donors = cls.COMPATIBILITY_MATRIX.get(recipient_type.upper(), [])
        return donor_unit_type.upper() in valid_donors
