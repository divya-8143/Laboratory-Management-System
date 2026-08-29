"""
AcuPath Enterprise LIS - Clinical Decision Support System (CDSS) & Delta Check Engine
Detects sudden physiological shifts, pre-analytical specimen mix-ups, and severe critical value escalations.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import datetime
import math


@dataclass
class DeltaCheckAlert:
    parameter_code: str
    parameter_name: str
    previous_value: float
    previous_datetime: datetime.datetime
    current_value: float
    current_datetime: datetime.datetime
    absolute_delta: float
    percentage_delta: float
    rate_delta_per_hour: float
    threshold_percent: float
    severity: str  # WARNING | CRITICAL_HOLD
    clinical_rationale: str


class DeltaCheckEngine:
    """Evaluates rate-of-change between historical results and current run."""

    DELTA_RULES = {
        "POTASSIUM": {"max_percent": 30.0, "timeframe_hours": 24, "rationale": "High delta suggests hemolysis, IV fluid contamination, or acute renal failure."},
        "HEMOGLOBIN": {"max_percent": 25.0, "timeframe_hours": 24, "rationale": "Sudden drop indicates acute hemorrhage or sample dilution."},
        "CREATININE": {"max_percent": 50.0, "timeframe_hours": 48, "rationale": "Sudden rise indicates Acute Kidney Injury (AKI)."},
        "PLATELETS": {"max_percent": 40.0, "timeframe_hours": 24, "rationale": "Sudden drop indicates EDTA-induced pseudothrombocytopenia or DIC."},
        "SODIUM": {"max_percent": 10.0, "timeframe_hours": 24, "rationale": "Rapid sodium shifts risk central pontine myelinolysis."}
    }

    @classmethod
    def evaluate_delta(
        cls,
        parameter_code: str,
        parameter_name: str,
        current_value: float,
        current_dt: datetime.datetime,
        previous_value: float,
        previous_dt: datetime.datetime
    ) -> Optional[DeltaCheckAlert]:
        code_upper = parameter_code.upper()
        rule = cls.DELTA_RULES.get(code_upper)
        if not rule:
            return None

        hours_diff = max(0.1, (current_dt - previous_dt).total_seconds() / 3600.0)
        if hours_diff > rule["timeframe_hours"]:
            return None

        abs_diff = abs(current_value - previous_value)
        pct_diff = (abs_diff / previous_value * 100.0) if previous_value != 0 else 0.0
        rate_per_hr = abs_diff / hours_diff

        if pct_diff > rule["max_percent"]:
            severity = "CRITICAL_HOLD" if pct_diff > (rule["max_percent"] * 1.5) else "WARNING"
            return DeltaCheckAlert(
                parameter_code=parameter_code,
                parameter_name=parameter_name,
                previous_value=previous_value,
                previous_datetime=previous_dt,
                current_value=current_value,
                current_datetime=current_dt,
                absolute_delta=round(abs_diff, 2),
                percentage_delta=round(pct_diff, 1),
                rate_delta_per_hour=round(rate_per_hr, 3),
                threshold_percent=rule["max_percent"],
                severity=severity,
                clinical_rationale=rule["rationale"]
            )
        return None
