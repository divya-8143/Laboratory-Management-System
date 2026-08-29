"""
AcuPath Enterprise LIS - Levey-Jennings Statistical Engine
Computes Levey-Jennings chart baselines, standard deviations, coefficient of variation (%CV),
CUSUM, and EWMA statistics for quality control visualizers.
"""

from typing import Dict, List, Optional, Any, Tuple
import math
import datetime


class LeveyJenningsEngine:
    """Computes statistical metrics for analytical quality control."""

    @staticmethod
    def calculate_statistics(values: List[float]) -> Dict[str, float]:
        if not values:
            return {"mean": 0.0, "sd": 0.0, "cv_percent": 0.0, "count": 0, "min": 0.0, "max": 0.0}

        n = len(values)
        mean = sum(values) / n

        if n < 2:
            sd = 0.0
        else:
            variance = sum((x - mean) ** 2 for x in values) / (n - 1)
            sd = math.sqrt(variance)

        cv_percent = (sd / mean * 100.0) if mean != 0 else 0.0

        return {
            "mean": round(mean, 4),
            "sd": round(sd, 4),
            "cv_percent": round(cv_percent, 2),
            "count": n,
            "min": round(min(values), 4),
            "max": round(max(values), 4),
            "sd_plus_1": round(mean + sd, 4),
            "sd_minus_1": round(mean - sd, 4),
            "sd_plus_2": round(mean + (2 * sd), 4),
            "sd_minus_2": round(mean - (2 * sd), 4),
            "sd_plus_3": round(mean + (3 * sd), 4),
            "sd_minus_3": round(mean - (3 * sd), 4)
        }

    @staticmethod
    def calculate_cusum(values: List[float], target_mean: float, target_sd: float, k: float = 0.5, h: float = 5.0) -> Dict[str, Any]:
        """Calculates Cumulative Sum (CUSUM) positive and negative charts for early systematic shift detection."""
        s_pos = [0.0]
        s_neg = [0.0]
        alarms = []

        for i, val in enumerate(values):
            z = (val - target_mean) / target_sd
            curr_pos = max(0.0, s_pos[-1] + z - k)
            curr_neg = max(0.0, s_neg[-1] - z - k)
            s_pos.append(curr_pos)
            s_neg.append(curr_neg)

            if curr_pos > h or curr_neg > h:
                alarms.append({"run_index": i, "cusum_pos": curr_pos, "cusum_neg": curr_neg, "threshold": h})

        return {
            "cusum_positive": s_pos[1:],
            "cusum_negative": s_neg[1:],
            "alarms": alarms
        }
