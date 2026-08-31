"""
AcuPath Enterprise LIS - LC-MS/MS Tandem Mass Spectrometry Quantitation Engine
Computes peak area ratios against internal standards and validates qualifier/quantifier ion ratios.
"""

from typing import Dict, List, Optional

class LCMSQuantitationEngine:
    @staticmethod
    def quantitate_analyte(quantifier_area: float, is_area: float, qualifier_area: float, response_factor: float = 1.0) -> Dict[str, Any]:
        area_ratio = quantifier_area / is_area if is_area != 0 else 0.0
        concentration_ng_ml = area_ratio * response_factor * 100.0
        ion_ratio = (qualifier_area / quantifier_area * 100.0) if quantifier_area != 0 else 0.0
        is_valid_ion_ratio = 15.0 <= ion_ratio <= 35.0

        return {
            "concentration_ng_ml": round(concentration_ng_ml, 2),
            "ion_ratio_percent": round(ion_ratio, 1),
            "ion_ratio_status": "PASS" if is_valid_ion_ratio else "FAIL_ION_RATIO",
            "confirmation": "CONFIRMED_POSITIVE" if is_valid_ion_ratio and concentration_ng_ml > 50.0 else "NEGATIVE"
        }
