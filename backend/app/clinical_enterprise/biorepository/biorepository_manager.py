"""
AcuPath Enterprise LIS - Cryogenic Sample Bio-Repository & Bio-Banking Subsystem
Tracks Ultra-Low Temperature (-80C) freezers, Liquid Nitrogen (LN2) tanks, 9x9 grid box mapping,
freeze-thaw cycle degradation, and bio-specimen donor consent governance.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import datetime
import uuid


@dataclass
class StorageLocation:
    freezer_unit_id: str = "ULT-FREEZER-01"
    temperature_celsius: float = -80.0
    rack_number: int = 1
    shelf_number: int = 2
    box_barcode: str = "BOX-ULT-80-042"
    grid_row: str = "C"      # A to I
    grid_column: int = 4     # 1 to 9
    position_code: str = "C04"


@dataclass
class BioSpecimen:
    specimen_id: str = field(default_factory=lambda: f"BIO-{uuid.uuid4().hex[:8].upper()}")
    patient_id: str = ""
    tissue_type: str = "SERUM_ALIQUOT"  # WHOLE_BLOOD | SERUM_ALIQUOT | DNA_EXTRACT | FRESH_FROZEN_TISSUE
    volume_microliters: float = 500.0
    freeze_thaw_cycles: int = 0
    max_allowable_cycles: int = 3
    donor_consent_verified: bool = True
    storage_location: StorageLocation = field(default_factory=StorageLocation)
    aliquot_date: datetime.date = field(default_factory=datetime.date.today)
    expiration_date: Optional[datetime.date] = None

    def record_thaw_cycle(self, technician_id: str, reason: str) -> bool:
        """Increments thaw cycle and verifies sample viability."""
        if self.freeze_thaw_cycles >= self.max_allowable_cycles:
            return False  # Viability compromised
        self.freeze_thaw_cycles += 1
        return True


class BioRepositoryManager:
    """Manages cryogenic storage hierarchies and automated rack optimization."""

    def __init__(self):
        self.specimen_index: Dict[str, BioSpecimen] = {}

    def store_specimen(self, specimen: BioSpecimen) -> Dict[str, Any]:
        self.specimen_index[specimen.specimen_id] = specimen
        return {
            "status": "STORED",
            "specimen_id": specimen.specimen_id,
            "location": f"{specimen.storage_location.freezer_unit_id}/{specimen.storage_location.box_barcode}/{specimen.storage_location.position_code}",
            "temp": f"{specimen.storage_location.temperature_celsius}C"
        }
