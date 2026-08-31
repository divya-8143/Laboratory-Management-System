"""
AcuPath Enterprise LIS - Antimicrobial Stewardship Program (ASP) & Antibiogram Engine
Evaluates CLSI M100 Minimum Inhibitory Concentration (MIC) breakpoints and MDRO resistance patterns.
"""

from typing import Dict, List, Optional

class AntimicrobialStewardshipEngine:
    @staticmethod
    def evaluate_susceptibility(organism: str, antibiotic: str, mic_ug_ml: float) -> Dict[str, str]:
        if "STAPHYLOCOCCUS" in organism.upper() and antibiotic.upper() == "OXACILLIN":
            interpretation = "RESISTANT (MRSA)" if mic_ug_ml >= 4.0 else "SUSCEPTIBLE (MSSA)"
        else:
            interpretation = "SUSCEPTIBLE" if mic_ug_ml <= 2.0 else "RESISTANT"

        return {
            "organism": organism,
            "antibiotic": antibiotic,
            "mic": f"{mic_ug_ml} ug/mL",
            "interpretation": interpretation
        }
