from typing import Optional, Tuple
from app.models.catalog import ReferenceRange, ParameterDataTypeEnum
from app.models.result import ResultFlagEnum


class ReferenceRangeEvaluator:
    @staticmethod
    def find_matching_range(
        ranges: list[ReferenceRange],
        patient_gender: str,
        patient_age_days: int
    ) -> Optional[ReferenceRange]:
        """
        Find best matching biological reference range for patient's gender and age in days.
        Prioritizes exact gender match over 'BOTH'.
        """
        gender_normalized = patient_gender.upper() if patient_gender else "BOTH"
        
        # 1. Look for exact gender + age range
        for r in ranges:
            if r.gender == gender_normalized and (r.age_min_days <= patient_age_days <= r.age_max_days):
                return r

        # 2. Look for BOTH gender + age range
        for r in ranges:
            if r.gender == "BOTH" and (r.age_min_days <= patient_age_days <= r.age_max_days):
                return r

        # 3. Fallback to any range with exact gender
        for r in ranges:
            if r.gender == gender_normalized:
                return r

        # 4. Fallback to first available range
        return ranges[0] if ranges else None

    @staticmethod
    def evaluate_result(
        data_type: ParameterDataTypeEnum,
        numeric_val: Optional[float],
        text_val: Optional[str],
        ref_range: Optional[ReferenceRange]
    ) -> Tuple[ResultFlagEnum, str, bool, bool]:
        """
        Evaluates test parameter result against clinical reference bounds.
        Returns: (flag, reference_range_display, is_abnormal, is_critical)
        """
        if not ref_range:
            display = "N/A"
            return ResultFlagEnum.NORMAL, display, False, False

        # Numeric parameter evaluation
        if data_type == ParameterDataTypeEnum.NUMERIC and numeric_val is not None:
            norm_min = ref_range.normal_min
            norm_max = ref_range.normal_max
            crit_low = ref_range.critical_low
            crit_high = ref_range.critical_high

            # Construct display string e.g. "13.8 - 17.2" or "< 200.0"
            if norm_min is not None and norm_max is not None:
                display = f"{norm_min} - {norm_max}"
            elif norm_min is not None:
                display = f">= {norm_min}"
            elif norm_max is not None:
                display = f"<= {norm_max}"
            else:
                display = "Reference bound not set"

            # Check critical bounds
            if crit_low is not None and numeric_val <= crit_low:
                return ResultFlagEnum.CRITICAL_LOW, display, True, True
            if crit_high is not None and numeric_val >= crit_high:
                return ResultFlagEnum.CRITICAL_HIGH, display, True, True

            # Check normal bounds
            if norm_min is not None and numeric_val < norm_min:
                return ResultFlagEnum.LOW, display, True, False
            if norm_max is not None and numeric_val > norm_max:
                return ResultFlagEnum.HIGH, display, True, False

            return ResultFlagEnum.NORMAL, display, False, False

        # Qualitative parameter evaluation
        if data_type == ParameterDataTypeEnum.QUALITATIVE:
            expected_normal = ref_range.qualitative_normal or "Negative"
            display = expected_normal
            current = (text_val or "").strip().lower()
            expected = expected_normal.strip().lower()

            if current == expected:
                return ResultFlagEnum.NORMAL, display, False, False
            else:
                return ResultFlagEnum.ABNORMAL, display, True, False

        display = ref_range.interpretation_text or "Standard Range"
        return ResultFlagEnum.NORMAL, display, False, False
