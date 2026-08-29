"""AcuPath Enterprise LIS - Master Biological Reference Range Dictionary"""
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class BiologicalInterval:
    gender: str
    age_min_years: float
    age_max_years: float
    normal_min: float
    normal_max: float
    critical_low: Optional[float]
    critical_high: Optional[float]
    unit: str

REFERENCE_INTERVALS_MASTER: Dict[str, List[BiologicalInterval]] = {
    'HEMOGLOBIN': [
        BiologicalInterval(gender='MALE', age_min_years=18, age_max_years=120, normal_min=13.5, normal_max=17.5, critical_low=7.0, critical_high=20.0, unit='g/dL'),
        BiologicalInterval(gender='FEMALE', age_min_years=18, age_max_years=120, normal_min=12.0, normal_max=15.5, critical_low=7.0, critical_high=20.0, unit='g/dL'),
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=1, normal_min=14.0, normal_max=24.0, critical_low=9.0, critical_high=25.0, unit='g/dL'),
        BiologicalInterval(gender='BOTH', age_min_years=1, age_max_years=18, normal_min=11.5, normal_max=15.5, critical_low=7.5, critical_high=19.0, unit='g/dL'),
    ],
    'HEMATOCRIT': [
        BiologicalInterval(gender='MALE', age_min_years=18, age_max_years=120, normal_min=38.8, normal_max=50.0, critical_low=20.0, critical_high=60.0, unit='%'),
        BiologicalInterval(gender='FEMALE', age_min_years=18, age_max_years=120, normal_min=34.9, normal_max=44.5, critical_low=20.0, critical_high=60.0, unit='%'),
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=18, normal_min=35.0, normal_max=45.0, critical_low=22.0, critical_high=55.0, unit='%'),
    ],
    'WHITE_BLOOD_CELLS': [
        BiologicalInterval(gender='BOTH', age_min_years=18, age_max_years=120, normal_min=4.5, normal_max=11.0, critical_low=2.0, critical_high=30.0, unit='10*3/uL'),
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=1, normal_min=9.0, normal_max=30.0, critical_low=4.0, critical_high=40.0, unit='10*3/uL'),
        BiologicalInterval(gender='BOTH', age_min_years=1, age_max_years=18, normal_min=5.0, normal_max=15.0, critical_low=2.5, critical_high=35.0, unit='10*3/uL'),
    ],
    'PLATELETS': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=150, normal_max=450, critical_low=20, critical_high=1000, unit='10*3/uL'),
    ],
    'FASTING_GLUCOSE': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=70, normal_max=99, critical_low=45, critical_high=450, unit='mg/dL'),
    ],
    'POSTPRANDIAL_GLUCOSE': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=70, normal_max=140, critical_low=45, critical_high=500, unit='mg/dL'),
    ],
    'HBA1C': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=4.0, normal_max=5.6, critical_low=3.5, critical_high=15.0, unit='%'),
    ],
    'SERUM_CREATININE': [
        BiologicalInterval(gender='MALE', age_min_years=18, age_max_years=120, normal_min=0.74, normal_max=1.35, critical_low=0.4, critical_high=5.0, unit='mg/dL'),
        BiologicalInterval(gender='FEMALE', age_min_years=18, age_max_years=120, normal_min=0.59, normal_max=1.04, critical_low=0.3, critical_high=5.0, unit='mg/dL'),
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=18, normal_min=0.3, normal_max=0.7, critical_low=0.2, critical_high=3.0, unit='mg/dL'),
    ],
    'BLOOD_UREA_NITROGEN': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=6, normal_max=20, critical_low=2, critical_high=80, unit='mg/dL'),
    ],
    'SERUM_SODIUM': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=135, normal_max=145, critical_low=120, critical_high=160, unit='mmol/L'),
    ],
    'SERUM_POTASSIUM': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=3.5, normal_max=5.0, critical_low=2.8, critical_high=6.2, unit='mmol/L'),
    ],
    'SERUM_CHLORIDE': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=96, normal_max=106, critical_low=80, critical_high=125, unit='mmol/L'),
    ],
    'SERUM_CALCIUM': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=8.5, normal_max=10.2, critical_low=6.0, critical_high=13.0, unit='mg/dL'),
    ],
    'SERUM_PHOSPHATE': [
        BiologicalInterval(gender='BOTH', age_min_years=18, age_max_years=120, normal_min=2.5, normal_max=4.5, critical_low=1.0, critical_high=8.0, unit='mg/dL'),
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=18, normal_min=4.0, normal_max=7.0, critical_low=1.5, critical_high=9.0, unit='mg/dL'),
    ],
    'SERUM_MAGNESIUM': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=1.7, normal_max=2.2, critical_low=1.0, critical_high=4.5, unit='mg/dL'),
    ],
    'ALT_ALANINE_AMINOTRANSFERASE': [
        BiologicalInterval(gender='MALE', age_min_years=0, age_max_years=120, normal_min=10, normal_max=40, critical_low=None, critical_high=400, unit='U/L'),
        BiologicalInterval(gender='FEMALE', age_min_years=0, age_max_years=120, normal_min=7, normal_max=35, critical_low=None, critical_high=400, unit='U/L'),
    ],
    'AST_ASPARTATE_AMINOTRANSFERASE': [
        BiologicalInterval(gender='MALE', age_min_years=0, age_max_years=120, normal_min=10, normal_max=40, critical_low=None, critical_high=400, unit='U/L'),
        BiologicalInterval(gender='FEMALE', age_min_years=0, age_max_years=120, normal_min=9, normal_max=32, critical_low=None, critical_high=400, unit='U/L'),
    ],
    'ALP_ALKALINE_PHOSPHATASE': [
        BiologicalInterval(gender='BOTH', age_min_years=18, age_max_years=120, normal_min=44, normal_max=147, critical_low=None, critical_high=500, unit='U/L'),
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=18, normal_min=100, normal_max=350, critical_low=None, critical_high=700, unit='U/L'),
    ],
    'TOTAL_BILIRUBIN': [
        BiologicalInterval(gender='BOTH', age_min_years=1, age_max_years=120, normal_min=0.1, normal_max=1.2, critical_low=None, critical_high=15.0, unit='mg/dL'),
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=1, normal_min=0.2, normal_max=12.0, critical_low=None, critical_high=20.0, unit='mg/dL'),
    ],
    'DIRECT_BILIRUBIN': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=0.0, normal_max=0.3, critical_low=None, critical_high=10.0, unit='mg/dL'),
    ],
    'TOTAL_PROTEIN': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=6.0, normal_max=8.3, critical_low=4.0, critical_high=11.0, unit='g/dL'),
    ],
    'SERUM_ALBUMIN': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=3.5, normal_max=5.5, critical_low=2.0, critical_high=6.5, unit='g/dL'),
    ],
    'TOTAL_CHOLESTEROL': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=120, normal_max=200, critical_low=None, critical_high=400, unit='mg/dL'),
    ],
    'TRIGLYCERIDES': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=40, normal_max=150, critical_low=None, critical_high=1000, unit='mg/dL'),
    ],
    'HDL_CHOLESTEROL': [
        BiologicalInterval(gender='MALE', age_min_years=0, age_max_years=120, normal_min=40, normal_max=70, critical_low=20, critical_high=None, unit='mg/dL'),
        BiologicalInterval(gender='FEMALE', age_min_years=0, age_max_years=120, normal_min=50, normal_max=80, critical_low=20, critical_high=None, unit='mg/dL'),
    ],
    'LDL_CHOLESTEROL': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=50, normal_max=100, critical_low=None, critical_high=250, unit='mg/dL'),
    ],
    'TSH_THYROID_STIMULATING_HORMONE': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=0.4, normal_max=4.0, critical_low=0.01, critical_high=20.0, unit='uIU/mL'),
    ],
    'FREE_T4': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=0.8, normal_max=1.8, critical_low=0.3, critical_high=4.0, unit='ng/dL'),
    ],
    'FREE_T3': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=2.3, normal_max=4.2, critical_low=1.0, critical_high=8.0, unit='pg/mL'),
    ],
    'PROTHROMBIN_TIME': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=11.0, normal_max=13.5, critical_low=8.0, critical_high=30.0, unit='seconds'),
    ],
    'INR': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=0.8, normal_max=1.1, critical_low=0.5, critical_high=4.5, unit='ratio'),
    ],
    'APTT': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=25.0, normal_max=35.0, critical_low=15.0, critical_high=90.0, unit='seconds'),
    ],
    'FIBRINOGEN': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=200, normal_max=400, critical_low=100, critical_high=800, unit='mg/dL'),
    ],
    'D_DIMER': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=0.0, normal_max=0.5, critical_low=None, critical_high=5.0, unit='ug/mL FEU'),
    ],
    'TROPONIN_I_HS': [
        BiologicalInterval(gender='MALE', age_min_years=0, age_max_years=120, normal_min=0.0, normal_max=0.034, critical_low=None, critical_high=0.1, unit='ng/mL'),
        BiologicalInterval(gender='FEMALE', age_min_years=0, age_max_years=120, normal_min=0.0, normal_max=0.016, critical_low=None, critical_high=0.1, unit='ng/mL'),
    ],
    'NT_PRO_BNP': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=50, normal_min=0, normal_max=125, critical_low=None, critical_high=1000, unit='pg/mL'),
        BiologicalInterval(gender='BOTH', age_min_years=50, age_max_years=75, normal_min=0, normal_max=450, critical_low=None, critical_high=2000, unit='pg/mL'),
        BiologicalInterval(gender='BOTH', age_min_years=75, age_max_years=120, normal_min=0, normal_max=900, critical_low=None, critical_high=5000, unit='pg/mL'),
    ],
    'SERUM_FERRITIN': [
        BiologicalInterval(gender='MALE', age_min_years=0, age_max_years=120, normal_min=24, normal_max=336, critical_low=10, critical_high=1500, unit='ng/mL'),
        BiologicalInterval(gender='FEMALE', age_min_years=0, age_max_years=120, normal_min=11, normal_max=307, critical_low=8, critical_high=1500, unit='ng/mL'),
    ],
    'VITAMIN_B12': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=200, normal_max=900, critical_low=100, critical_high=2000, unit='pg/mL'),
    ],
    'SERUM_FOLATE': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=3.1, normal_max=17.5, critical_low=2.0, critical_high=25.0, unit='ng/mL'),
    ],
    'VITAMIN_D_25_OH': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=30.0, normal_max=100.0, critical_low=10.0, critical_high=150.0, unit='ng/mL'),
    ],
    'URIC_ACID': [
        BiologicalInterval(gender='MALE', age_min_years=0, age_max_years=120, normal_min=3.4, normal_max=7.0, critical_low=1.5, critical_high=12.0, unit='mg/dL'),
        BiologicalInterval(gender='FEMALE', age_min_years=0, age_max_years=120, normal_min=2.4, normal_max=6.0, critical_low=1.0, critical_high=11.0, unit='mg/dL'),
    ],
    'C_REACTIVE_PROTEIN': [
        BiologicalInterval(gender='BOTH', age_min_years=0, age_max_years=120, normal_min=0.0, normal_max=0.8, critical_low=None, critical_high=10.0, unit='mg/dL'),
    ],
    'ESR_WESTERGREN': [
        BiologicalInterval(gender='MALE', age_min_years=0, age_max_years=50, normal_min=0, normal_max=15, critical_low=None, critical_high=60, unit='mm/hr'),
        BiologicalInterval(gender='MALE', age_min_years=50, age_max_years=120, normal_min=0, normal_max=20, critical_low=None, critical_high=70, unit='mm/hr'),
        BiologicalInterval(gender='FEMALE', age_min_years=0, age_max_years=50, normal_min=0, normal_max=20, critical_low=None, critical_high=70, unit='mm/hr'),
        BiologicalInterval(gender='FEMALE', age_min_years=50, age_max_years=120, normal_min=0, normal_max=30, critical_low=None, critical_high=80, unit='mm/hr'),
    ],
}
