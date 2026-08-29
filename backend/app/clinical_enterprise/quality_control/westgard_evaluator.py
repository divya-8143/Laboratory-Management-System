"""
AcuPath Enterprise LIS - Westgard Multirule Statistical Quality Control Engine
Evaluates clinical laboratory QC runs against standard Westgard Multirules:
- 1:2s Warning (1 control value exceeds Mean +/- 2SD)
- 1:3s Rejection (1 control value exceeds Mean +/- 3SD) -> Random error
- 2:2s Rejection (2 consecutive control values exceed Mean + 2SD or Mean - 2SD) -> Systematic error
- R:4s Rejection (1 control exceeds +2SD and another exceeds -2SD in same run) -> Random error
- 4:1s Rejection (4 consecutive control values exceed Mean + 1SD or Mean - 1SD) -> Systematic error
- 10:x Rejection (10 consecutive control values fall on one side of Mean) -> Systematic shift
- 7:T Trend Rule (7 consecutive values continually increasing or decreasing) -> Calibration drift
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import enum
import math


class WestgardRuleStatus(str, enum.Enum):
    PASSED = "PASSED"
    WARNING = "WARNING"
    REJECTED = "REJECTED"


class ErrorType(str, enum.Enum):
    NONE = "NONE"
    RANDOM_ERROR = "RANDOM_ERROR"
    SYSTEMATIC_ERROR = "SYSTEMATIC_ERROR"
    SYSTEMATIC_SHIFT = "SYSTEMATIC_SHIFT"
    CALIBRATION_DRIFT = "CALIBRATION_DRIFT"


@dataclass
class WestgardViolation:
    rule_code: str
    rule_name: str
    status: WestgardRuleStatus
    error_type: ErrorType
    description: str
    run_indices_involved: List[int]
    recommended_action: str


class WestgardEvaluator:
    """Statistical QC evaluator for automated clinical run validation."""

    @staticmethod
    def evaluate_run(
        target_mean: float,
        target_sd: float,
        current_value: float,
        historical_values: List[float],
        across_levels_values: Optional[List[float]] = None
    ) -> Tuple[WestgardRuleStatus, List[WestgardViolation]]:
        """
        Evaluates the current QC run using single-run and historical run sequences.
        historical_values must be in chronological order (most recent is at end).
        """
        violations: List[WestgardViolation] = []
        all_values = historical_values + [current_value]
        n = len(all_values)

        z_scores = [(v - target_mean) / target_sd for v in all_values]
        current_z = z_scores[-1]

        # Rule 1: 1_2s Warning
        if abs(current_z) > 2.0:
            violations.append(WestgardViolation(
                rule_code="1:2s",
                rule_name="1-2s Warning Rule",
                status=WestgardRuleStatus.WARNING,
                error_type=ErrorType.NONE,
                description=f"Control value {current_value:.3f} deviates {current_z:.2f} SD from target mean ({target_mean}). Check subsequent rules.",
                run_indices_involved=[n - 1],
                recommended_action="Inspect system for potential drift, but run may proceed unless rejection rules trigger."
            ))

        # Rule 2: 1_3s Rejection
        if abs(current_z) > 3.0:
            violations.append(WestgardViolation(
                rule_code="1:3s",
                rule_name="1-3s Rejection Rule",
                status=WestgardRuleStatus.REJECTED,
                error_type=ErrorType.RANDOM_ERROR,
                description=f"Control value {current_value:.3f} exceeded 3 standard deviations ({current_z:.2f} SD).",
                run_indices_involved=[n - 1],
                recommended_action="Reject analytical run. Re-assay sample and check for bubbles, pipetting errors, or reagent deterioration."
            ))

        # Rule 3: 2_2s Rejection (Within-run across 2 levels or across 2 consecutive runs on same level)
        if n >= 2:
            if (z_scores[-1] > 2.0 and z_scores[-2] > 2.0) or (z_scores[-1] < -2.0 and z_scores[-2] < -2.0):
                violations.append(WestgardViolation(
                    rule_code="2:2s",
                    rule_name="2-2s Rejection Rule",
                    status=WestgardRuleStatus.REJECTED,
                    error_type=ErrorType.SYSTEMATIC_ERROR,
                    description=f"2 consecutive runs exceeded 2 SD on the same side of mean ({z_scores[-2]:.2f} SD, {z_scores[-1]:.2f} SD).",
                    run_indices_involved=[n - 2, n - 1],
                    recommended_action="Reject analytical run. Check instrument calibration and reagent lot integrity."
                ))

        # Rule 4: R_4s Rejection (Range between 2 controls exceeds 4 SD)
        if n >= 2:
            if (z_scores[-1] > 2.0 and z_scores[-2] < -2.0) or (z_scores[-1] < -2.0 and z_scores[-2] > 2.0):
                violations.append(WestgardViolation(
                    rule_code="R:4s",
                    rule_name="R-4s Range Rejection Rule",
                    status=WestgardRuleStatus.REJECTED,
                    error_type=ErrorType.RANDOM_ERROR,
                    description=f"Difference between 2 consecutive controls exceeds 4 SD (Range = {abs(z_scores[-1] - z_scores[-2]):.2f} SD).",
                    run_indices_involved=[n - 2, n - 1],
                    recommended_action="Reject analytical run. Random error detected. Re-calibrate and re-run control aliquots."
                ))

        # Rule 5: 4_1s Rejection (4 consecutive runs exceeding +1 SD or -1 SD)
        if n >= 4:
            last_4_z = z_scores[-4:]
            if all(z > 1.0 for z in last_4_z) or all(z < -1.0 for z in last_4_z):
                violations.append(WestgardViolation(
                    rule_code="4:1s",
                    rule_name="4-1s Rejection Rule",
                    status=WestgardRuleStatus.REJECTED,
                    error_type=ErrorType.SYSTEMATIC_ERROR,
                    description="4 consecutive controls exceed 1 SD on the same side of the target mean.",
                    run_indices_involved=list(range(n - 4, n)),
                    recommended_action="Reject analytical run. Systematic shift detected. Perform recalibration or maintenance."
                ))

        # Rule 6: 10_x Rejection (10 consecutive runs on same side of mean)
        if n >= 10:
            last_10_z = z_scores[-10:]
            if all(z > 0 for z in last_10_z) or all(z < 0 for z in last_10_z):
                violations.append(WestgardViolation(
                    rule_code="10:x",
                    rule_name="10-x Systematic Shift Rule",
                    status=WestgardRuleStatus.REJECTED,
                    error_type=ErrorType.SYSTEMATIC_SHIFT,
                    description="10 consecutive controls fall on one side of the mean, indicating a baseline calibration shift.",
                    run_indices_involved=list(range(n - 10, n)),
                    recommended_action="Perform instrument recalibration and check lamp/optical detector baselines."
                ))

        # Rule 7: 7_T Trend Rule (7 consecutive values continually increasing or decreasing)
        if n >= 7:
            last_7 = all_values[-7:]
            is_increasing = all(last_7[i] < last_7[i + 1] for i in range(len(last_7) - 1))
            is_decreasing = all(last_7[i] > last_7[i + 1] for i in range(len(last_7) - 1))
            if is_increasing or is_decreasing:
                violations.append(WestgardViolation(
                    rule_code="7:T",
                    rule_name="7-Trend Rule",
                    status=WestgardRuleStatus.REJECTED,
                    error_type=ErrorType.CALIBRATION_DRIFT,
                    description="7 consecutive values show a continuous trend in one direction (Calibration Drift).",
                    run_indices_involved=list(range(n - 7, n)),
                    recommended_action="Inspect reagent stability, light source degradation, or environmental temperature variations."
                ))

        has_rejection = any(v.status == WestgardRuleStatus.REJECTED for v in violations)
        has_warning = any(v.status == WestgardRuleStatus.WARNING for v in violations)

        if has_rejection:
            return WestgardRuleStatus.REJECTED, violations
        elif has_warning:
            return WestgardRuleStatus.WARNING, violations
        return WestgardRuleStatus.PASSED, []
