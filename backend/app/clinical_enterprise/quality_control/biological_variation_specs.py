"""AcuPath Enterprise LIS - Biological Variation & Desirable Quality Specifications Database"""
from typing import Dict, Any

BIOLOGICAL_VARIATION_DATABASE = {
    'GLUCOSE': {
        'within_subject_cvi': 4.9,
        'between_subject_cvg': 6.9,
        'total_variation_cvt': 8.4,
        'desirable_imprecision_i': 2.3,
        'desirable_bias_b': 2.3,
        'desirable_total_allowable_error_tea': 6.1
    },
    'CHOLESTEROL': {
        'within_subject_cvi': 5.4,
        'between_subject_cvg': 15.2,
        'total_variation_cvt': 16.1,
        'desirable_imprecision_i': 2.7,
        'desirable_bias_b': 4.0,
        'desirable_total_allowable_error_tea': 8.5
    },
    'TRIGLYCERIDES': {
        'within_subject_cvi': 19.9,
        'between_subject_cvg': 37.8,
        'total_variation_cvt': 42.7,
        'desirable_imprecision_i': 10.0,
        'desirable_bias_b': 10.7,
        'desirable_total_allowable_error_tea': 27.2
    },
    'HDL_CHOLESTEROL': {
        'within_subject_cvi': 7.1,
        'between_subject_cvg': 19.9,
        'total_variation_cvt': 21.1,
        'desirable_imprecision_i': 3.6,
        'desirable_bias_b': 5.3,
        'desirable_total_allowable_error_tea': 11.2
    },
    'LDL_CHOLESTEROL': {
        'within_subject_cvi': 7.8,
        'between_subject_cvg': 25.0,
        'total_variation_cvt': 26.2,
        'desirable_imprecision_i': 3.9,
        'desirable_bias_b': 6.6,
        'desirable_total_allowable_error_tea': 13.0
    },
    'CREATININE': {
        'within_subject_cvi': 4.3,
        'between_subject_cvg': 14.7,
        'total_variation_cvt': 15.3,
        'desirable_imprecision_i': 2.2,
        'desirable_bias_b': 3.8,
        'desirable_total_allowable_error_tea': 7.4
    },
    'UREA_NITROGEN': {
        'within_subject_cvi': 12.3,
        'between_subject_cvg': 18.2,
        'total_variation_cvt': 22.0,
        'desirable_imprecision_i': 6.2,
        'desirable_bias_b': 5.5,
        'desirable_total_allowable_error_tea': 15.7
    },
    'URIC_ACID': {
        'within_subject_cvi': 8.6,
        'between_subject_cvg': 17.5,
        'total_variation_cvt': 19.5,
        'desirable_imprecision_i': 4.3,
        'desirable_bias_b': 4.9,
        'desirable_total_allowable_error_tea': 12.0
    },
    'SODIUM': {
        'within_subject_cvi': 0.6,
        'between_subject_cvg': 0.7,
        'total_variation_cvt': 0.9,
        'desirable_imprecision_i': 0.3,
        'desirable_bias_b': 0.2,
        'desirable_total_allowable_error_tea': 0.7
    },
    'POTASSIUM': {
        'within_subject_cvi': 4.6,
        'between_subject_cvg': 5.6,
        'total_variation_cvt': 7.2,
        'desirable_imprecision_i': 2.3,
        'desirable_bias_b': 1.8,
        'desirable_total_allowable_error_tea': 5.6
    },
    'CHLORIDE': {
        'within_subject_cvi': 1.2,
        'between_subject_cvg': 1.5,
        'total_variation_cvt': 1.9,
        'desirable_imprecision_i': 0.6,
        'desirable_bias_b': 0.5,
        'desirable_total_allowable_error_tea': 1.5
    },
    'CALCIUM': {
        'within_subject_cvi': 1.7,
        'between_subject_cvg': 2.8,
        'total_variation_cvt': 3.3,
        'desirable_imprecision_i': 0.9,
        'desirable_bias_b': 0.8,
        'desirable_total_allowable_error_tea': 2.3
    },
    'PHOSPHORUS': {
        'within_subject_cvi': 8.5,
        'between_subject_cvg': 9.6,
        'total_variation_cvt': 12.8,
        'desirable_imprecision_i': 4.3,
        'desirable_bias_b': 3.2,
        'desirable_total_allowable_error_tea': 10.3
    },
    'MAGNESIUM': {
        'within_subject_cvi': 3.0,
        'between_subject_cvg': 6.4,
        'total_variation_cvt': 7.1,
        'desirable_imprecision_i': 1.5,
        'desirable_bias_b': 1.8,
        'desirable_total_allowable_error_tea': 4.3
    },
    'TOTAL_PROTEIN': {
        'within_subject_cvi': 2.6,
        'between_subject_cvg': 4.7,
        'total_variation_cvt': 5.4,
        'desirable_imprecision_i': 1.3,
        'desirable_bias_b': 1.3,
        'desirable_total_allowable_error_tea': 3.5
    },
    'ALBUMIN': {
        'within_subject_cvi': 2.6,
        'between_subject_cvg': 4.8,
        'total_variation_cvt': 5.5,
        'desirable_imprecision_i': 1.3,
        'desirable_bias_b': 1.4,
        'desirable_total_allowable_error_tea': 3.5
    },
    'TOTAL_BILIRUBIN': {
        'within_subject_cvi': 21.8,
        'between_subject_cvg': 30.6,
        'total_variation_cvt': 37.6,
        'desirable_imprecision_i': 10.9,
        'desirable_bias_b': 9.4,
        'desirable_total_allowable_error_tea': 27.4
    },
    'DIRECT_BILIRUBIN': {
        'within_subject_cvi': 36.8,
        'between_subject_cvg': 43.2,
        'total_variation_cvt': 56.8,
        'desirable_imprecision_i': 18.4,
        'desirable_bias_b': 14.2,
        'desirable_total_allowable_error_tea': 44.6
    },
    'ALT_ALANINE_AMINOTRANSFERASE': {
        'within_subject_cvi': 19.4,
        'between_subject_cvg': 38.2,
        'total_variation_cvt': 42.8,
        'desirable_imprecision_i': 9.7,
        'desirable_bias_b': 10.7,
        'desirable_total_allowable_error_tea': 26.7
    },
    'AST_ASPARTATE_AMINOTRANSFERASE': {
        'within_subject_cvi': 12.3,
        'between_subject_cvg': 23.1,
        'total_variation_cvt': 26.2,
        'desirable_imprecision_i': 6.2,
        'desirable_bias_b': 6.6,
        'desirable_total_allowable_error_tea': 16.8
    },
    'ALP_ALKALINE_PHOSPHATASE': {
        'within_subject_cvi': 6.4,
        'between_subject_cvg': 25.8,
        'total_variation_cvt': 26.6,
        'desirable_imprecision_i': 3.2,
        'desirable_bias_b': 6.6,
        'desirable_total_allowable_error_tea': 11.9
    },
    'GGT_GAMMA_GLUTAMYLTRANSFERASE': {
        'within_subject_cvi': 13.8,
        'between_subject_cvg': 42.1,
        'total_variation_cvt': 44.3,
        'desirable_imprecision_i': 6.9,
        'desirable_bias_b': 11.1,
        'desirable_total_allowable_error_tea': 22.5
    },
    'LDH_LACTATE_DEHYDROGENASE': {
        'within_subject_cvi': 7.0,
        'between_subject_cvg': 15.0,
        'total_variation_cvt': 16.6,
        'desirable_imprecision_i': 3.5,
        'desirable_bias_b': 4.1,
        'desirable_total_allowable_error_tea': 9.9
    },
    'CK_CREATINE_KINASE': {
        'within_subject_cvi': 22.8,
        'between_subject_cvg': 40.0,
        'total_variation_cvt': 46.0,
        'desirable_imprecision_i': 11.4,
        'desirable_bias_b': 11.5,
        'desirable_total_allowable_error_tea': 30.3
    },
    'AMYLASE': {
        'within_subject_cvi': 8.7,
        'between_subject_cvg': 18.0,
        'total_variation_cvt': 20.0,
        'desirable_imprecision_i': 4.4,
        'desirable_bias_b': 5.0,
        'desirable_total_allowable_error_tea': 12.3
    },
    'LIPASE': {
        'within_subject_cvi': 20.0,
        'between_subject_cvg': 30.0,
        'total_variation_cvt': 36.0,
        'desirable_imprecision_i': 10.0,
        'desirable_bias_b': 9.0,
        'desirable_total_allowable_error_tea': 25.5
    },
    'HEMOGLOBIN': {
        'within_subject_cvi': 2.8,
        'between_subject_cvg': 6.8,
        'total_variation_cvt': 7.4,
        'desirable_imprecision_i': 1.4,
        'desirable_bias_b': 1.8,
        'desirable_total_allowable_error_tea': 4.1
    },
    'HEMATOCRIT': {
        'within_subject_cvi': 2.8,
        'between_subject_cvg': 7.3,
        'total_variation_cvt': 7.8,
        'desirable_imprecision_i': 1.4,
        'desirable_bias_b': 2.0,
        'desirable_total_allowable_error_tea': 4.3
    },
    'RBC_RED_BLOOD_CELLS': {
        'within_subject_cvi': 3.2,
        'between_subject_cvg': 6.0,
        'total_variation_cvt': 6.8,
        'desirable_imprecision_i': 1.6,
        'desirable_bias_b': 1.7,
        'desirable_total_allowable_error_tea': 4.3
    },
    'WBC_WHITE_BLOOD_CELLS': {
        'within_subject_cvi': 10.9,
        'between_subject_cvg': 17.5,
        'total_variation_cvt': 20.6,
        'desirable_imprecision_i': 5.5,
        'desirable_bias_b': 5.2,
        'desirable_total_allowable_error_tea': 14.3
    },
    'PLATELETS': {
        'within_subject_cvi': 9.1,
        'between_subject_cvg': 21.6,
        'total_variation_cvt': 23.5,
        'desirable_imprecision_i': 4.6,
        'desirable_bias_b': 5.9,
        'desirable_total_allowable_error_tea': 13.5
    },
    'MCV_MEAN_CORPUSCULAR_VOLUME': {
        'within_subject_cvi': 1.4,
        'between_subject_cvg': 4.7,
        'total_variation_cvt': 4.9,
        'desirable_imprecision_i': 0.7,
        'desirable_bias_b': 1.2,
        'desirable_total_allowable_error_tea': 2.4
    },
    'MCH_MEAN_CORPUSCULAR_HEMOGLOBIN': {
        'within_subject_cvi': 1.6,
        'between_subject_cvg': 5.5,
        'total_variation_cvt': 5.7,
        'desirable_imprecision_i': 0.8,
        'desirable_bias_b': 1.4,
        'desirable_total_allowable_error_tea': 2.7
    },
    'MCHC_CONCENTRATION': {
        'within_subject_cvi': 1.3,
        'between_subject_cvg': 3.8,
        'total_variation_cvt': 4.0,
        'desirable_imprecision_i': 0.7,
        'desirable_bias_b': 1.0,
        'desirable_total_allowable_error_tea': 2.2
    },
    'NEUTROPHILS_PERCENT': {
        'within_subject_cvi': 14.6,
        'between_subject_cvg': 19.3,
        'total_variation_cvt': 24.2,
        'desirable_imprecision_i': 7.3,
        'desirable_bias_b': 6.1,
        'desirable_total_allowable_error_tea': 18.1
    },
    'LYMPHOCYTES_PERCENT': {
        'within_subject_cvi': 10.5,
        'between_subject_cvg': 17.2,
        'total_variation_cvt': 20.1,
        'desirable_imprecision_i': 5.3,
        'desirable_bias_b': 5.0,
        'desirable_total_allowable_error_tea': 13.7
    },
    'MONOCYTES_PERCENT': {
        'within_subject_cvi': 17.7,
        'between_subject_cvg': 24.1,
        'total_variation_cvt': 29.9,
        'desirable_imprecision_i': 8.9,
        'desirable_bias_b': 7.5,
        'desirable_total_allowable_error_tea': 22.2
    },
    'EOSINOPHILS_PERCENT': {
        'within_subject_cvi': 23.0,
        'between_subject_cvg': 40.0,
        'total_variation_cvt': 46.1,
        'desirable_imprecision_i': 11.5,
        'desirable_bias_b': 11.5,
        'desirable_total_allowable_error_tea': 30.5
    },
    'BASOPHILS_PERCENT': {
        'within_subject_cvi': 25.0,
        'between_subject_cvg': 45.0,
        'total_variation_cvt': 51.5,
        'desirable_imprecision_i': 12.5,
        'desirable_bias_b': 12.9,
        'desirable_total_allowable_error_tea': 33.5
    },
    'RETICULOCYTES_PERCENT': {
        'within_subject_cvi': 18.0,
        'between_subject_cvg': 28.0,
        'total_variation_cvt': 33.3,
        'desirable_imprecision_i': 9.0,
        'desirable_bias_b': 8.3,
        'desirable_total_allowable_error_tea': 23.2
    },
    'ESR_SEDIMENTATION_RATE': {
        'within_subject_cvi': 20.0,
        'between_subject_cvg': 30.0,
        'total_variation_cvt': 36.1,
        'desirable_imprecision_i': 10.0,
        'desirable_bias_b': 9.0,
        'desirable_total_allowable_error_tea': 25.5
    },
    'PT_PROTHROMBIN_TIME': {
        'within_subject_cvi': 4.0,
        'between_subject_cvg': 6.8,
        'total_variation_cvt': 7.9,
        'desirable_imprecision_i': 2.0,
        'desirable_bias_b': 2.0,
        'desirable_total_allowable_error_tea': 5.3
    },
    'APTT_THROMBOPLASTIN_TIME': {
        'within_subject_cvi': 3.0,
        'between_subject_cvg': 6.0,
        'total_variation_cvt': 6.7,
        'desirable_imprecision_i': 1.5,
        'desirable_bias_b': 1.7,
        'desirable_total_allowable_error_tea': 4.2
    },
    'FIBRINOGEN': {
        'within_subject_cvi': 10.7,
        'between_subject_cvg': 15.8,
        'total_variation_cvt': 19.1,
        'desirable_imprecision_i': 5.4,
        'desirable_bias_b': 4.8,
        'desirable_total_allowable_error_tea': 13.7
    },
    'D_DIMER': {
        'within_subject_cvi': 15.0,
        'between_subject_cvg': 25.0,
        'total_variation_cvt': 29.2,
        'desirable_imprecision_i': 7.5,
        'desirable_bias_b': 7.3,
        'desirable_total_allowable_error_tea': 19.7
    },
    'TSH_THYROID_STIMULATING_HORMONE': {
        'within_subject_cvi': 19.3,
        'between_subject_cvg': 24.6,
        'total_variation_cvt': 31.3,
        'desirable_imprecision_i': 9.7,
        'desirable_bias_b': 7.8,
        'desirable_total_allowable_error_tea': 23.8
    },
    'FREE_T4_THYROXINE': {
        'within_subject_cvi': 6.3,
        'between_subject_cvg': 12.0,
        'total_variation_cvt': 13.6,
        'desirable_imprecision_i': 3.2,
        'desirable_bias_b': 3.4,
        'desirable_total_allowable_error_tea': 8.7
    },
    'FREE_T3_TRIIODOTHYRONINE': {
        'within_subject_cvi': 7.8,
        'between_subject_cvg': 14.2,
        'total_variation_cvt': 16.2,
        'desirable_imprecision_i': 3.9,
        'desirable_bias_b': 4.1,
        'desirable_total_allowable_error_tea': 10.5
    },
    'PSA_PROSTATE_SPECIFIC_ANTIGEN': {
        'within_subject_cvi': 14.0,
        'between_subject_cvg': 18.0,
        'total_variation_cvt': 22.8,
        'desirable_imprecision_i': 7.0,
        'desirable_bias_b': 5.7,
        'desirable_total_allowable_error_tea': 17.3
    },
    'FERRITIN': {
        'within_subject_cvi': 15.0,
        'between_subject_cvg': 18.0,
        'total_variation_cvt': 23.4,
        'desirable_imprecision_i': 7.5,
        'desirable_bias_b': 5.9,
        'desirable_total_allowable_error_tea': 18.3
    },
    'VITAMIN_B12': {
        'within_subject_cvi': 15.0,
        'between_subject_cvg': 22.0,
        'total_variation_cvt': 26.6,
        'desirable_imprecision_i': 7.5,
        'desirable_bias_b': 6.7,
        'desirable_total_allowable_error_tea': 19.1
    },
    'FOLATE': {
        'within_subject_cvi': 18.0,
        'between_subject_cvg': 25.0,
        'total_variation_cvt': 30.8,
        'desirable_imprecision_i': 9.0,
        'desirable_bias_b': 7.7,
        'desirable_total_allowable_error_tea': 22.6
    },
    'VITAMIN_D_25_OH': {
        'within_subject_cvi': 11.5,
        'between_subject_cvg': 23.4,
        'total_variation_cvt': 26.1,
        'desirable_imprecision_i': 5.8,
        'desirable_bias_b': 6.5,
        'desirable_total_allowable_error_tea': 16.1
    },
    'HBA1C_GLYCATED_HEMOGLOBIN': {
        'within_subject_cvi': 1.9,
        'between_subject_cvg': 5.7,
        'total_variation_cvt': 6.0,
        'desirable_imprecision_i': 1.0,
        'desirable_bias_b': 1.5,
        'desirable_total_allowable_error_tea': 3.2
    },
    'C_REACTIVE_PROTEIN': {
        'within_subject_cvi': 42.2,
        'between_subject_cvg': 76.3,
        'total_variation_cvt': 87.2,
        'desirable_imprecision_i': 21.1,
        'desirable_bias_b': 21.8,
        'desirable_total_allowable_error_tea': 56.6
    },
    'HIGH_SENSITIVITY_CRP': {
        'within_subject_cvi': 30.0,
        'between_subject_cvg': 60.0,
        'total_variation_cvt': 67.1,
        'desirable_imprecision_i': 15.0,
        'desirable_bias_b': 16.8,
        'desirable_total_allowable_error_tea': 41.6
    },
    'TROPONIN_I': {
        'within_subject_cvi': 14.0,
        'between_subject_cvg': 20.0,
        'total_variation_cvt': 24.4,
        'desirable_imprecision_i': 7.0,
        'desirable_bias_b': 6.1,
        'desirable_total_allowable_error_tea': 17.7
    },
    'TROPONIN_T': {
        'within_subject_cvi': 15.0,
        'between_subject_cvg': 22.0,
        'total_variation_cvt': 26.6,
        'desirable_imprecision_i': 7.5,
        'desirable_bias_b': 6.7,
        'desirable_total_allowable_error_tea': 19.1
    },
    'BNP_BRAIN_NATRIURETIC_PEPTIDE': {
        'within_subject_cvi': 33.0,
        'between_subject_cvg': 45.0,
        'total_variation_cvt': 55.8,
        'desirable_imprecision_i': 16.5,
        'desirable_bias_b': 14.0,
        'desirable_total_allowable_error_tea': 41.2
    },
    'NT_PRO_BNP': {
        'within_subject_cvi': 30.0,
        'between_subject_cvg': 42.0,
        'total_variation_cvt': 51.6,
        'desirable_imprecision_i': 15.0,
        'desirable_bias_b': 12.9,
        'desirable_total_allowable_error_tea': 37.7
    },
}
