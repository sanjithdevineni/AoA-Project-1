"""Naive baseline for validating divide-and-conquer maximum subarray."""

from __future__ import annotations

from typing import List, Tuple


def max_subarray_naive(values: List[float]) -> Tuple[int, int, float]:
    """Brute-force maximum subarray via exhaustive enumeration.

    Args:
        values: List of daily profit/loss values.

    Returns:
        Tuple (start_idx, end_idx, max_sum) where indices are inclusive.

    Edge Cases:
        Returns (-1, -1, 0.0) for empty array.
        Returns (0, 0, values[0]) for single element.

    Complexity:
        O(n²) time, O(1) space.
    """
    if not values:
        return -1, -1, 0.0

    n = len(values)
    max_sum = float("-inf")
    best_start = 0
    best_end = 0

    for i in range(n):
        current_sum = 0.0
        for j in range(i, n):
            current_sum += values[j]
            if current_sum > max_sum:
                max_sum = current_sum
                best_start = i
                best_end = j

    return best_start, best_end, max_sum


__all__ = ["max_subarray_naive"]