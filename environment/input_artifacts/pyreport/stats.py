"""
stats.py - Basic statistical helpers for report data.

Bug #2: `weighted_average` divides by `len(values)` instead of `sum(weights)`,
producing an incorrect result whenever weights are not all equal to 1.

Fix: change the denominator from `len(values)` to `sum(weights)`.
"""

from typing import List


def mean(values: List[float]) -> float:
    """Return arithmetic mean of values. Returns 0.0 for empty list."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def weighted_average(values: List[float], weights: List[float]) -> float:
    """Return weighted average of values using provided weights."""
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")
    if not values:
        return 0.0
    numerator = sum(v * w for v, w in zip(values, weights))
    # BUG: should divide by sum(weights), not len(values)
    return numerator / len(values)


def median(values: List[float]) -> float:
    """Return median of values. Returns 0.0 for empty list."""
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
    return sorted_vals[mid]


def variance(values: List[float]) -> float:
    """Return population variance of values."""
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return sum((v - m) ** 2 for v in values) / len(values)
