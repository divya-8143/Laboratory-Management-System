"""
AcuPath Enterprise LIS - Digital Pathology & DICOM Part 10 Parser
Handles DICOM WSI (Whole Slide Imaging) metadata, Tile Pyramids, and SVS/NDPI Slide Manifests.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import uuid
import datetime


@dataclass
class WSISlideMetadata:
    slide_id: str
    accession_number: str
    patient_id: str
    stain_type: str = "H&E"  # H&E | IHC_HER2 | IHC_ER | IHC_PR | KI67 | PAS | GRAM
    magnification: str = "40X"
    resolution_mpp: float = 0.25  # Microns Per Pixel
    image_width: int = 100000
    image_height: int = 80000
    pyramid_levels: int = 6
    tissue_type: str = "Breast Biopsy"
    pathologist_id: Optional[str] = None
    annotations_count: int = 0
