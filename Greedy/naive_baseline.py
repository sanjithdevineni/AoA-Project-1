"""Naive baseline for validating greedy EV trip planning."""

from __future__ import annotations

from typing import List, Tuple


def min_stops_dp(sorted_positions: List[float], D: float, R: float) -> Tuple[int, List[float]]:
    """Return minimal number of charging stops via quadratic DP.

    Args:
        sorted_positions: Strictly increasing station mile markers in (0, D).
        D: Trip destination distance from the origin.
        R: Maximum distance on a full charge.

    Returns:
        A tuple ``(stop_count, stops)`` with the optimal number of stops and one
        corresponding sequence of station mile markers.

    Edge Cases:
        Returns (0, []) when D == 0 or directly reachable, and raises
        ValueError("infeasible") when no feasible sequence exists.

    Raises:
        ValueError: If the inputs are invalid or the route is infeasible.
    """

    _validate_inputs(sorted_positions, D, R)
    if D == 0:
        return 0, []

    augmented = [0.0, *sorted_positions, float(D)]

    n = len(augmented)
    dest_idx = n - 1
    unreachable = n + 1

    stops_needed = [unreachable] * n
    predecessor = [-1] * n
    stops_needed[0] = 0

    for j in range(1, n):
        best = unreachable
        best_pred = -1
        for i in range(j):
            if augmented[j] - augmented[i] > R:
                continue
            proposed = stops_needed[i]
            if j != dest_idx:
                proposed += 1
            if proposed < best:
                best = proposed
                best_pred = i
        stops_needed[j] = best
        predecessor[j] = best_pred

    if stops_needed[dest_idx] >= unreachable:
        raise ValueError("infeasible")

    stops: List[float] = []
    cursor = dest_idx
    while cursor > 0:
        pred = predecessor[cursor]
        if pred == -1:
            break
        if cursor != dest_idx:
            stops.append(augmented[cursor])
        cursor = pred
    stops.reverse()

    return stops_needed[dest_idx], stops


__all__ = ["min_stops_dp"]


def _validate_inputs(positions: List[float], D: float, R: float) -> None:
    if R <= 0:
        raise ValueError("range must be positive")
    if D < 0:
        raise ValueError("destination must be non-negative")

    last = 0.0
    for pos in positions:
        if pos <= 0 or pos >= D:
            raise ValueError("station positions must lie strictly between 0 and D")
        if pos <= last:
            raise ValueError("station positions must be strictly increasing")
        last = pos
