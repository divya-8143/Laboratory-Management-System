"""AcuPath Enterprise LIS - Complete ASTM Analyzer Telemetry Profiles"""
from typing import Dict, List, Any

class TelemetryProfile_Sysmex_XN_Series:
    """Telemetry dictionary for Sysmex_XN_Series (Hematology)"""
    INSTRUMENT_NAME = 'Sysmex_XN_Series'
    DEPARTMENT = 'Hematology'
    SUPPORTED_PARAMETERS = ['WBC', 'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'PLT', 'NEUT_PCT', 'LYMPH_PCT', 'MONO_PCT', 'EO_PCT', 'BASO_PCT', 'RETIC_PCT', 'IG_PCT']
    PARAMETER_SPECIFICATIONS: Dict[str, Dict[str, Any]] = {
        'WBC': {'code': 'WBC', 'astm_channel': 'CHANNEL_WBC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'RBC': {'code': 'RBC', 'astm_channel': 'CHANNEL_RBC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HGB': {'code': 'HGB', 'astm_channel': 'CHANNEL_HGB', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HCT': {'code': 'HCT', 'astm_channel': 'CHANNEL_HCT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MCV': {'code': 'MCV', 'astm_channel': 'CHANNEL_MCV', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MCH': {'code': 'MCH', 'astm_channel': 'CHANNEL_MCH', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MCHC': {'code': 'MCHC', 'astm_channel': 'CHANNEL_MCHC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PLT': {'code': 'PLT', 'astm_channel': 'CHANNEL_PLT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'NEUT_PCT': {'code': 'NEUT_PCT', 'astm_channel': 'CHANNEL_NEUT_PCT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'LYMPH_PCT': {'code': 'LYMPH_PCT', 'astm_channel': 'CHANNEL_LYMPH_PCT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MONO_PCT': {'code': 'MONO_PCT', 'astm_channel': 'CHANNEL_MONO_PCT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'EO_PCT': {'code': 'EO_PCT', 'astm_channel': 'CHANNEL_EO_PCT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'BASO_PCT': {'code': 'BASO_PCT', 'astm_channel': 'CHANNEL_BASO_PCT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'RETIC_PCT': {'code': 'RETIC_PCT', 'astm_channel': 'CHANNEL_RETIC_PCT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'IG_PCT': {'code': 'IG_PCT', 'astm_channel': 'CHANNEL_IG_PCT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
    }

class TelemetryProfile_Roche_Cobas_8000:
    """Telemetry dictionary for Roche_Cobas_8000 (Clinical Chemistry)"""
    INSTRUMENT_NAME = 'Roche_Cobas_8000'
    DEPARTMENT = 'Clinical Chemistry'
    SUPPORTED_PARAMETERS = ['GLU', 'BUN', 'CREAT', 'NA', 'K', 'CL', 'CO2', 'CA', 'PHOS', 'MG', 'ALT', 'AST', 'ALP', 'GGT', 'TBIL', 'DBIL', 'TP', 'ALB', 'URIC_ACID', 'LDH']
    PARAMETER_SPECIFICATIONS: Dict[str, Dict[str, Any]] = {
        'GLU': {'code': 'GLU', 'astm_channel': 'CHANNEL_GLU', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'BUN': {'code': 'BUN', 'astm_channel': 'CHANNEL_BUN', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CREAT': {'code': 'CREAT', 'astm_channel': 'CHANNEL_CREAT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'NA': {'code': 'NA', 'astm_channel': 'CHANNEL_NA', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'K': {'code': 'K', 'astm_channel': 'CHANNEL_K', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CL': {'code': 'CL', 'astm_channel': 'CHANNEL_CL', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CO2': {'code': 'CO2', 'astm_channel': 'CHANNEL_CO2', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CA': {'code': 'CA', 'astm_channel': 'CHANNEL_CA', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PHOS': {'code': 'PHOS', 'astm_channel': 'CHANNEL_PHOS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MG': {'code': 'MG', 'astm_channel': 'CHANNEL_MG', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'ALT': {'code': 'ALT', 'astm_channel': 'CHANNEL_ALT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'AST': {'code': 'AST', 'astm_channel': 'CHANNEL_AST', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'ALP': {'code': 'ALP', 'astm_channel': 'CHANNEL_ALP', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'GGT': {'code': 'GGT', 'astm_channel': 'CHANNEL_GGT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'TBIL': {'code': 'TBIL', 'astm_channel': 'CHANNEL_TBIL', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'DBIL': {'code': 'DBIL', 'astm_channel': 'CHANNEL_DBIL', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'TP': {'code': 'TP', 'astm_channel': 'CHANNEL_TP', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'ALB': {'code': 'ALB', 'astm_channel': 'CHANNEL_ALB', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'URIC_ACID': {'code': 'URIC_ACID', 'astm_channel': 'CHANNEL_URIC_ACID', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'LDH': {'code': 'LDH', 'astm_channel': 'CHANNEL_LDH', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
    }

class TelemetryProfile_Abbott_Architect_ci8200:
    """Telemetry dictionary for Abbott_Architect_ci8200 (Integrated Chemistry/Immunoassay)"""
    INSTRUMENT_NAME = 'Abbott_Architect_ci8200'
    DEPARTMENT = 'Integrated Chemistry/Immunoassay'
    SUPPORTED_PARAMETERS = ['TSH', 'FT4', 'FT3', 'TROPONIN_I', 'CKMB', 'BNP', 'PRO_BNP', 'MYOGLOBIN', 'FERRITIN', 'VITAMIN_B12', 'FOLATE', 'PSA_TOTAL', 'PSA_FREE', 'CEA', 'CA_125', 'CA_19_9', 'AFP', 'HCG_TOTAL']
    PARAMETER_SPECIFICATIONS: Dict[str, Dict[str, Any]] = {
        'TSH': {'code': 'TSH', 'astm_channel': 'CHANNEL_TSH', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'FT4': {'code': 'FT4', 'astm_channel': 'CHANNEL_FT4', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'FT3': {'code': 'FT3', 'astm_channel': 'CHANNEL_FT3', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'TROPONIN_I': {'code': 'TROPONIN_I', 'astm_channel': 'CHANNEL_TROPONIN_I', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CKMB': {'code': 'CKMB', 'astm_channel': 'CHANNEL_CKMB', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'BNP': {'code': 'BNP', 'astm_channel': 'CHANNEL_BNP', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PRO_BNP': {'code': 'PRO_BNP', 'astm_channel': 'CHANNEL_PRO_BNP', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MYOGLOBIN': {'code': 'MYOGLOBIN', 'astm_channel': 'CHANNEL_MYOGLOBIN', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'FERRITIN': {'code': 'FERRITIN', 'astm_channel': 'CHANNEL_FERRITIN', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'VITAMIN_B12': {'code': 'VITAMIN_B12', 'astm_channel': 'CHANNEL_VITAMIN_B12', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'FOLATE': {'code': 'FOLATE', 'astm_channel': 'CHANNEL_FOLATE', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PSA_TOTAL': {'code': 'PSA_TOTAL', 'astm_channel': 'CHANNEL_PSA_TOTAL', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PSA_FREE': {'code': 'PSA_FREE', 'astm_channel': 'CHANNEL_PSA_FREE', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CEA': {'code': 'CEA', 'astm_channel': 'CHANNEL_CEA', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CA_125': {'code': 'CA_125', 'astm_channel': 'CHANNEL_CA_125', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CA_19_9': {'code': 'CA_19_9', 'astm_channel': 'CHANNEL_CA_19_9', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'AFP': {'code': 'AFP', 'astm_channel': 'CHANNEL_AFP', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HCG_TOTAL': {'code': 'HCG_TOTAL', 'astm_channel': 'CHANNEL_HCG_TOTAL', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
    }

class TelemetryProfile_Beckman_DxH_900:
    """Telemetry dictionary for Beckman_DxH_900 (High-Volume Hematology)"""
    INSTRUMENT_NAME = 'Beckman_DxH_900'
    DEPARTMENT = 'High-Volume Hematology'
    SUPPORTED_PARAMETERS = ['WBC', 'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'RDW_CV', 'RDW_SD', 'PLT', 'MPV', 'PCT', 'PDW', 'NE_ABS', 'LY_ABS', 'MO_ABS', 'EO_ABS', 'BA_ABS']
    PARAMETER_SPECIFICATIONS: Dict[str, Dict[str, Any]] = {
        'WBC': {'code': 'WBC', 'astm_channel': 'CHANNEL_WBC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'RBC': {'code': 'RBC', 'astm_channel': 'CHANNEL_RBC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HGB': {'code': 'HGB', 'astm_channel': 'CHANNEL_HGB', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HCT': {'code': 'HCT', 'astm_channel': 'CHANNEL_HCT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MCV': {'code': 'MCV', 'astm_channel': 'CHANNEL_MCV', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MCH': {'code': 'MCH', 'astm_channel': 'CHANNEL_MCH', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MCHC': {'code': 'MCHC', 'astm_channel': 'CHANNEL_MCHC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'RDW_CV': {'code': 'RDW_CV', 'astm_channel': 'CHANNEL_RDW_CV', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'RDW_SD': {'code': 'RDW_SD', 'astm_channel': 'CHANNEL_RDW_SD', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PLT': {'code': 'PLT', 'astm_channel': 'CHANNEL_PLT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MPV': {'code': 'MPV', 'astm_channel': 'CHANNEL_MPV', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PCT': {'code': 'PCT', 'astm_channel': 'CHANNEL_PCT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PDW': {'code': 'PDW', 'astm_channel': 'CHANNEL_PDW', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'NE_ABS': {'code': 'NE_ABS', 'astm_channel': 'CHANNEL_NE_ABS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'LY_ABS': {'code': 'LY_ABS', 'astm_channel': 'CHANNEL_LY_ABS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MO_ABS': {'code': 'MO_ABS', 'astm_channel': 'CHANNEL_MO_ABS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'EO_ABS': {'code': 'EO_ABS', 'astm_channel': 'CHANNEL_EO_ABS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'BA_ABS': {'code': 'BA_ABS', 'astm_channel': 'CHANNEL_BA_ABS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
    }

class TelemetryProfile_BioRad_Variant_II:
    """Telemetry dictionary for BioRad_Variant_II (HPLC Glycohemoglobin)"""
    INSTRUMENT_NAME = 'BioRad_Variant_II'
    DEPARTMENT = 'HPLC Glycohemoglobin'
    SUPPORTED_PARAMETERS = ['HBA1C_PERCENT', 'HBA1C_IFCC', 'ESTIMATED_AVG_GLUCOSE', 'HB_VARIANT_DETECTED', 'HBF_PERCENT', 'HBA2_PERCENT']
    PARAMETER_SPECIFICATIONS: Dict[str, Dict[str, Any]] = {
        'HBA1C_PERCENT': {'code': 'HBA1C_PERCENT', 'astm_channel': 'CHANNEL_HBA1C_PERCENT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HBA1C_IFCC': {'code': 'HBA1C_IFCC', 'astm_channel': 'CHANNEL_HBA1C_IFCC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'ESTIMATED_AVG_GLUCOSE': {'code': 'ESTIMATED_AVG_GLUCOSE', 'astm_channel': 'CHANNEL_ESTIMATED_AVG_GLUCOSE', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HB_VARIANT_DETECTED': {'code': 'HB_VARIANT_DETECTED', 'astm_channel': 'CHANNEL_HB_VARIANT_DETECTED', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HBF_PERCENT': {'code': 'HBF_PERCENT', 'astm_channel': 'CHANNEL_HBF_PERCENT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HBA2_PERCENT': {'code': 'HBA2_PERCENT', 'astm_channel': 'CHANNEL_HBA2_PERCENT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
    }

class TelemetryProfile_Mindray_BS_800M:
    """Telemetry dictionary for Mindray_BS_800M (Modular Chemistry)"""
    INSTRUMENT_NAME = 'Mindray_BS_800M'
    DEPARTMENT = 'Modular Chemistry'
    SUPPORTED_PARAMETERS = ['ALB', 'ALP', 'ALT', 'AMYLASE', 'AST', 'DIRECT_BILIRUBIN', 'TOTAL_BILIRUBIN', 'CALCIUM', 'CHOLESTEROL', 'HDL_C', 'LDL_C', 'TRIGLYCERIDES', 'CREATININE', 'GLUCOSE', 'IRON', 'TIBC', 'LACTATE', 'LIPASE', 'MAGNESIUM', 'PHOSPHORUS', 'TOTAL_PROTEIN', 'UREA', 'URIC_ACID']
    PARAMETER_SPECIFICATIONS: Dict[str, Dict[str, Any]] = {
        'ALB': {'code': 'ALB', 'astm_channel': 'CHANNEL_ALB', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'ALP': {'code': 'ALP', 'astm_channel': 'CHANNEL_ALP', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'ALT': {'code': 'ALT', 'astm_channel': 'CHANNEL_ALT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'AMYLASE': {'code': 'AMYLASE', 'astm_channel': 'CHANNEL_AMYLASE', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'AST': {'code': 'AST', 'astm_channel': 'CHANNEL_AST', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'DIRECT_BILIRUBIN': {'code': 'DIRECT_BILIRUBIN', 'astm_channel': 'CHANNEL_DIRECT_BILIRUBIN', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'TOTAL_BILIRUBIN': {'code': 'TOTAL_BILIRUBIN', 'astm_channel': 'CHANNEL_TOTAL_BILIRUBIN', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CALCIUM': {'code': 'CALCIUM', 'astm_channel': 'CHANNEL_CALCIUM', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CHOLESTEROL': {'code': 'CHOLESTEROL', 'astm_channel': 'CHANNEL_CHOLESTEROL', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HDL_C': {'code': 'HDL_C', 'astm_channel': 'CHANNEL_HDL_C', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'LDL_C': {'code': 'LDL_C', 'astm_channel': 'CHANNEL_LDL_C', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'TRIGLYCERIDES': {'code': 'TRIGLYCERIDES', 'astm_channel': 'CHANNEL_TRIGLYCERIDES', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CREATININE': {'code': 'CREATININE', 'astm_channel': 'CHANNEL_CREATININE', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'GLUCOSE': {'code': 'GLUCOSE', 'astm_channel': 'CHANNEL_GLUCOSE', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'IRON': {'code': 'IRON', 'astm_channel': 'CHANNEL_IRON', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'TIBC': {'code': 'TIBC', 'astm_channel': 'CHANNEL_TIBC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'LACTATE': {'code': 'LACTATE', 'astm_channel': 'CHANNEL_LACTATE', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'LIPASE': {'code': 'LIPASE', 'astm_channel': 'CHANNEL_LIPASE', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MAGNESIUM': {'code': 'MAGNESIUM', 'astm_channel': 'CHANNEL_MAGNESIUM', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PHOSPHORUS': {'code': 'PHOSPHORUS', 'astm_channel': 'CHANNEL_PHOSPHORUS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'TOTAL_PROTEIN': {'code': 'TOTAL_PROTEIN', 'astm_channel': 'CHANNEL_TOTAL_PROTEIN', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'UREA': {'code': 'UREA', 'astm_channel': 'CHANNEL_UREA', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'URIC_ACID': {'code': 'URIC_ACID', 'astm_channel': 'CHANNEL_URIC_ACID', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
    }

class TelemetryProfile_Siemens_ADVIA_2120i:
    """Telemetry dictionary for Siemens_ADVIA_2120i (Optical Hematology)"""
    INSTRUMENT_NAME = 'Siemens_ADVIA_2120i'
    DEPARTMENT = 'Optical Hematology'
    SUPPORTED_PARAMETERS = ['WBC_PEROX', 'WBC_BASO', 'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'CHCM', 'HDW', 'PLT_OPTICAL', 'MPV', 'LUC_PCT', 'LUC_ABS', 'MYELOCYTES', 'METAMYELOCYTES', 'BAND_CELLS']
    PARAMETER_SPECIFICATIONS: Dict[str, Dict[str, Any]] = {
        'WBC_PEROX': {'code': 'WBC_PEROX', 'astm_channel': 'CHANNEL_WBC_PEROX', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'WBC_BASO': {'code': 'WBC_BASO', 'astm_channel': 'CHANNEL_WBC_BASO', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'RBC': {'code': 'RBC', 'astm_channel': 'CHANNEL_RBC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HGB': {'code': 'HGB', 'astm_channel': 'CHANNEL_HGB', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HCT': {'code': 'HCT', 'astm_channel': 'CHANNEL_HCT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MCV': {'code': 'MCV', 'astm_channel': 'CHANNEL_MCV', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MCH': {'code': 'MCH', 'astm_channel': 'CHANNEL_MCH', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MCHC': {'code': 'MCHC', 'astm_channel': 'CHANNEL_MCHC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CHCM': {'code': 'CHCM', 'astm_channel': 'CHANNEL_CHCM', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HDW': {'code': 'HDW', 'astm_channel': 'CHANNEL_HDW', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PLT_OPTICAL': {'code': 'PLT_OPTICAL', 'astm_channel': 'CHANNEL_PLT_OPTICAL', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MPV': {'code': 'MPV', 'astm_channel': 'CHANNEL_MPV', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'LUC_PCT': {'code': 'LUC_PCT', 'astm_channel': 'CHANNEL_LUC_PCT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'LUC_ABS': {'code': 'LUC_ABS', 'astm_channel': 'CHANNEL_LUC_ABS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MYELOCYTES': {'code': 'MYELOCYTES', 'astm_channel': 'CHANNEL_MYELOCYTES', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'METAMYELOCYTES': {'code': 'METAMYELOCYTES', 'astm_channel': 'CHANNEL_METAMYELOCYTES', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'BAND_CELLS': {'code': 'BAND_CELLS', 'astm_channel': 'CHANNEL_BAND_CELLS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
    }

class TelemetryProfile_Diagnostica_Stago_STA_Max:
    """Telemetry dictionary for Diagnostica_Stago_STA_Max (Automated Hemostasis)"""
    INSTRUMENT_NAME = 'Diagnostica_Stago_STA_Max'
    DEPARTMENT = 'Automated Hemostasis'
    SUPPORTED_PARAMETERS = ['PT_SECONDS', 'PT_INR', 'PT_PERCENT', 'APTT_SECONDS', 'APTT_RATIO', 'FIBRINOGEN_CLAUSS', 'THROMBIN_TIME', 'D_DIMER_FEU', 'ANTITHROMBIN_III', 'PROTEIN_C_ACTIVITY', 'PROTEIN_S_ACTIVITY', 'FACTOR_VIII', 'FACTOR_IX', 'VON_WILLEBRAND_AG']
    PARAMETER_SPECIFICATIONS: Dict[str, Dict[str, Any]] = {
        'PT_SECONDS': {'code': 'PT_SECONDS', 'astm_channel': 'CHANNEL_PT_SECONDS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PT_INR': {'code': 'PT_INR', 'astm_channel': 'CHANNEL_PT_INR', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PT_PERCENT': {'code': 'PT_PERCENT', 'astm_channel': 'CHANNEL_PT_PERCENT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'APTT_SECONDS': {'code': 'APTT_SECONDS', 'astm_channel': 'CHANNEL_APTT_SECONDS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'APTT_RATIO': {'code': 'APTT_RATIO', 'astm_channel': 'CHANNEL_APTT_RATIO', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'FIBRINOGEN_CLAUSS': {'code': 'FIBRINOGEN_CLAUSS', 'astm_channel': 'CHANNEL_FIBRINOGEN_CLAUSS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'THROMBIN_TIME': {'code': 'THROMBIN_TIME', 'astm_channel': 'CHANNEL_THROMBIN_TIME', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'D_DIMER_FEU': {'code': 'D_DIMER_FEU', 'astm_channel': 'CHANNEL_D_DIMER_FEU', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'ANTITHROMBIN_III': {'code': 'ANTITHROMBIN_III', 'astm_channel': 'CHANNEL_ANTITHROMBIN_III', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PROTEIN_C_ACTIVITY': {'code': 'PROTEIN_C_ACTIVITY', 'astm_channel': 'CHANNEL_PROTEIN_C_ACTIVITY', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PROTEIN_S_ACTIVITY': {'code': 'PROTEIN_S_ACTIVITY', 'astm_channel': 'CHANNEL_PROTEIN_S_ACTIVITY', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'FACTOR_VIII': {'code': 'FACTOR_VIII', 'astm_channel': 'CHANNEL_FACTOR_VIII', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'FACTOR_IX': {'code': 'FACTOR_IX', 'astm_channel': 'CHANNEL_FACTOR_IX', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'VON_WILLEBRAND_AG': {'code': 'VON_WILLEBRAND_AG', 'astm_channel': 'CHANNEL_VON_WILLEBRAND_AG', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
    }

class TelemetryProfile_Horiba_Yumizen_H2500:
    """Telemetry dictionary for Horiba_Yumizen_H2500 (Hematology Automation)"""
    INSTRUMENT_NAME = 'Horiba_Yumizen_H2500'
    DEPARTMENT = 'Hematology Automation'
    SUPPORTED_PARAMETERS = ['WBC', 'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'PLT', 'NEU', 'LYM', 'MON', 'EOS', 'BAS', 'LIC', 'ALY']
    PARAMETER_SPECIFICATIONS: Dict[str, Dict[str, Any]] = {
        'WBC': {'code': 'WBC', 'astm_channel': 'CHANNEL_WBC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'RBC': {'code': 'RBC', 'astm_channel': 'CHANNEL_RBC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HGB': {'code': 'HGB', 'astm_channel': 'CHANNEL_HGB', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HCT': {'code': 'HCT', 'astm_channel': 'CHANNEL_HCT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MCV': {'code': 'MCV', 'astm_channel': 'CHANNEL_MCV', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MCH': {'code': 'MCH', 'astm_channel': 'CHANNEL_MCH', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MCHC': {'code': 'MCHC', 'astm_channel': 'CHANNEL_MCHC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PLT': {'code': 'PLT', 'astm_channel': 'CHANNEL_PLT', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'NEU': {'code': 'NEU', 'astm_channel': 'CHANNEL_NEU', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'LYM': {'code': 'LYM', 'astm_channel': 'CHANNEL_LYM', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'MON': {'code': 'MON', 'astm_channel': 'CHANNEL_MON', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'EOS': {'code': 'EOS', 'astm_channel': 'CHANNEL_EOS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'BAS': {'code': 'BAS', 'astm_channel': 'CHANNEL_BAS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'LIC': {'code': 'LIC', 'astm_channel': 'CHANNEL_LIC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'ALY': {'code': 'ALY', 'astm_channel': 'CHANNEL_ALY', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
    }

class TelemetryProfile_Radiometer_ABL90_FLEX:
    """Telemetry dictionary for Radiometer_ABL90_FLEX (Blood Gas Analyzer)"""
    INSTRUMENT_NAME = 'Radiometer_ABL90_FLEX'
    DEPARTMENT = 'Blood Gas Analyzer'
    SUPPORTED_PARAMETERS = ['PH', 'PCO2', 'PO2', 'HCO3_ACTUAL', 'HCO3_STANDARD', 'BASE_EXCESS', 'SO2', 'FO2HB', 'FCOHB', 'FMETHB', 'FHHB', 'CNA', 'CK', 'CCA', 'CCL', 'CGLU', 'CLAC', 'CTHB']
    PARAMETER_SPECIFICATIONS: Dict[str, Dict[str, Any]] = {
        'PH': {'code': 'PH', 'astm_channel': 'CHANNEL_PH', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PCO2': {'code': 'PCO2', 'astm_channel': 'CHANNEL_PCO2', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'PO2': {'code': 'PO2', 'astm_channel': 'CHANNEL_PO2', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HCO3_ACTUAL': {'code': 'HCO3_ACTUAL', 'astm_channel': 'CHANNEL_HCO3_ACTUAL', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'HCO3_STANDARD': {'code': 'HCO3_STANDARD', 'astm_channel': 'CHANNEL_HCO3_STANDARD', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'BASE_EXCESS': {'code': 'BASE_EXCESS', 'astm_channel': 'CHANNEL_BASE_EXCESS', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'SO2': {'code': 'SO2', 'astm_channel': 'CHANNEL_SO2', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'FO2HB': {'code': 'FO2HB', 'astm_channel': 'CHANNEL_FO2HB', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'FCOHB': {'code': 'FCOHB', 'astm_channel': 'CHANNEL_FCOHB', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'FMETHB': {'code': 'FMETHB', 'astm_channel': 'CHANNEL_FMETHB', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'FHHB': {'code': 'FHHB', 'astm_channel': 'CHANNEL_FHHB', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CNA': {'code': 'CNA', 'astm_channel': 'CHANNEL_CNA', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CK': {'code': 'CK', 'astm_channel': 'CHANNEL_CK', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CCA': {'code': 'CCA', 'astm_channel': 'CHANNEL_CCA', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CCL': {'code': 'CCL', 'astm_channel': 'CHANNEL_CCL', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CGLU': {'code': 'CGLU', 'astm_channel': 'CHANNEL_CGLU', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CLAC': {'code': 'CLAC', 'astm_channel': 'CHANNEL_CLAC', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
        'CTHB': {'code': 'CTHB', 'astm_channel': 'CHANNEL_CTHB', 'precision': 2, 'unit': 'SI_UNIT', 'calibration_frequency_days': 30, 'qc_frequency_hours': 8},
    }

