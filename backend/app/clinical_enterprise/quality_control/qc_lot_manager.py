"""
AcuPath Enterprise LIS - Quality Control Lot Manager
Tracks multi-level control materials (Level 1 Normal, Level 2 Low, Level 3 High),
lot expiration dates, open-vial stability, and parallel cross-over testing for lot transition.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import datetime
import uuid


@dataclass
class QCLot:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    lot_number: str = ""
    control_name: str = ""  # e.g., Bio-Rad Lyphochek Assayed Chemistry Control
    manufacturer: str = "Bio-Rad Laboratories"
    level: str = "LEVEL_1_NORMAL"  # LEVEL_1_NORMAL | LEVEL_2_LOW | LEVEL_3_HIGH
    target_mean: float = 0.0
    target_sd: float = 0.0
    acceptable_min: float = 0.0
    acceptable_max: float = 0.0
    unit: str = "mg/dL"
    parameter_code: str = "GLU"
    expiration_date: Optional[datetime.date] = None
    open_vial_stability_days: int = 14
    opened_at: Optional[datetime.datetime] = None
    is_active: bool = True
    crossover_data_points: List[float] = field(default_factory=list)

    def is_expired(self) -> bool:
        today = datetime.date.today()
        if self.expiration_date and today > self.expiration_date:
            return True
        if self.opened_at:
            open_days = (datetime.datetime.utcnow() - self.opened_at).days
            if open_days > self.open_vial_stability_days:
                return True
        return False
