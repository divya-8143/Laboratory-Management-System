import pytest
from app.services.reference_range_evaluator import ReferenceRangeEvaluator
from app.models.catalog import ReferenceRange, ParameterDataTypeEnum
from app.models.result import ResultFlagEnum


def test_reference_range_evaluator_numeric_bounds():
    """Test normal, low, high, and critical triggers for numeric clinical parameters."""
    ref_range = ReferenceRange(
        id="ref-1",
        parameter_id="param-hgb",
        gender="MALE",
        age_min_days=0,
        age_max_days=40000,
        normal_min=13.8,
        normal_max=17.2,
        critical_low=7.0,
        critical_high=20.0
    )

    # 1. Normal Value (15.0)
    flag, disp, is_abn, is_crit = ReferenceRangeEvaluator.evaluate_result(
        ParameterDataTypeEnum.NUMERIC, 15.0, None, ref_range
    )
    assert flag == ResultFlagEnum.NORMAL
    assert not is_abn
    assert not is_crit
    assert disp == "13.8 - 17.2"

    # 2. Low Value (12.0)
    flag, disp, is_abn, is_crit = ReferenceRangeEvaluator.evaluate_result(
        ParameterDataTypeEnum.NUMERIC, 12.0, None, ref_range
    )
    assert flag == ResultFlagEnum.LOW
    assert is_abn
    assert not is_crit

    # 3. Critical Low Value (6.5)
    flag, disp, is_abn, is_crit = ReferenceRangeEvaluator.evaluate_result(
        ParameterDataTypeEnum.NUMERIC, 6.5, None, ref_range
    )
    assert flag == ResultFlagEnum.CRITICAL_LOW
    assert is_abn
    assert is_crit

    # 4. Critical High Value (21.5)
    flag, disp, is_abn, is_crit = ReferenceRangeEvaluator.evaluate_result(
        ParameterDataTypeEnum.NUMERIC, 21.5, None, ref_range
    )
    assert flag == ResultFlagEnum.CRITICAL_HIGH
    assert is_abn
    assert is_crit


def test_reference_range_evaluator_qualitative():
    """Test qualitative parameters (e.g. Negative vs Reactive)."""
    ref_range = ReferenceRange(
        id="ref-qual",
        parameter_id="param-hiv",
        gender="BOTH",
        qualitative_normal="Negative"
    )

    # Normal finding
    flag, disp, is_abn, is_crit = ReferenceRangeEvaluator.evaluate_result(
        ParameterDataTypeEnum.QUALITATIVE, None, "Negative", ref_range
    )
    assert flag == ResultFlagEnum.NORMAL
    assert not is_abn

    # Abnormal finding
    flag, disp, is_abn, is_crit = ReferenceRangeEvaluator.evaluate_result(
        ParameterDataTypeEnum.QUALITATIVE, None, "Reactive", ref_range
    )
    assert flag == ResultFlagEnum.ABNORMAL
    assert is_abn
