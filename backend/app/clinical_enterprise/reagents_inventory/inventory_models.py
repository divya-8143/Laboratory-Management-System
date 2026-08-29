"""
AcuPath Enterprise LIS - Laboratory Reagents & Consumables Inventory Models
Tracks Reagents, Calibrators, Quality Controls, Specimen Containers, and Consumables.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import datetime
import uuid


@dataclass
class ReagentLot:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reagent_code: str = ""
    reagent_name: str = ""
    lot_number: str = ""
    catalog_number: str = ""
    manufacturer: str = "Roche Diagnostics"
    storage_condition: str = "2_TO_8_CELSIUS"  # 2_TO_8_CELSIUS | MINUS_20_CELSIUS | ROOM_TEMP
    tests_per_kit: int = 500
    tests_remaining: int = 500
    volume_ml: float = 100.0
    dead_volume_ml: float = 2.5
    cost_per_test: float = 1.25
    expiration_date: Optional[datetime.date] = None
    onboard_instrument_id: Optional[str] = None
    is_onboard: bool = False
    is_active: bool = True

    def deduct_tests(self, count: int = 1) -> bool:
        if self.tests_remaining >= count:
            self.tests_remaining -= count
            return True
        return False
