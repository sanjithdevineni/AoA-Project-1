"""Unit tests for the greedy EV planning algorithms."""

from __future__ import annotations

import math
import random
import unittest

from Greedy.ev_greedy import plan_stops, plan_stops_sorted
from Greedy.naive_baseline import min_stops_dp


class TestEVGreedy(unittest.TestCase):
    def test_feasible_case(self) -> None:
        positions = [20.0, 35.0, 50.0, 70.0, 90.0]
        stops = plan_stops_sorted(positions, D=100.0, R=40.0)
        self.assertEqual(stops, [35.0, 70.0])

    def test_destination_within_range(self) -> None:
        self.assertEqual(plan_stops_sorted([], D=30.0, R=40.0), [])

    def test_destination_exactly_reachable_without_stations(self) -> None:
        self.assertEqual(plan_stops_sorted([], D=50.0, R=50.0), [])

    def test_unreachable_gap(self) -> None:
        positions = [30.0, 70.0, 120.0]
        with self.assertRaises(ValueError):
            plan_stops_sorted(positions, D=150.0, R=40.0)

    def test_edge_reachability(self) -> None:
        positions = [40.0, 80.0]
        stops = plan_stops_sorted(positions, D=120.0, R=40.0)
        self.assertEqual(stops, [40.0, 80.0])

    def test_random_small_instances(self) -> None:
        rng = random.Random(0)
        for trial in range(30):
            with self.subTest(trial=trial):
                n = rng.randint(0, 60)
                D = 500.0
                positions = [
                    ((i + rng.random()) / (n + 1)) * D for i in range(n)
                ]
                positions.sort()
                R = rng.uniform(20.0, 120.0)

                try:
                    greedy_stops = plan_stops_sorted(positions, D, R)
                    greedy_count = len(greedy_stops)
                except ValueError:
                    greedy_count = None

                try:
                    optimal_count, _ = min_stops_dp(positions, D, R)
                except ValueError:
                    optimal_count = None

                self.assertEqual(greedy_count, optimal_count)

    def test_plan_stops_matches_sorted(self) -> None:
        rng = random.Random(1)
        positions = [
            ((i + rng.random()) / 11) * 200.0 for i in range(10)
        ]
        shuffled = list(positions)
        rng.shuffle(shuffled)
        greedy_unsorted = plan_stops(shuffled, D=200.0, R=60.0, assume_sorted=False)
        greedy_sorted = plan_stops_sorted(positions, D=200.0, R=60.0)
        self.assertEqual(greedy_unsorted, greedy_sorted)

    def test_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            plan_stops_sorted([10.0, 20.0], D=-5.0, R=40.0)
        with self.assertRaises(ValueError):
            plan_stops_sorted([10.0, 20.0], D=60.0, R=0.0)
        with self.assertRaises(ValueError):
            plan_stops_sorted([10.0, 10.0], D=60.0, R=30.0)
        with self.assertRaises(ValueError):
            plan_stops_sorted([10.0, 65.0], D=60.0, R=30.0)
        with self.assertRaises(ValueError):
            min_stops_dp([10.0, 10.0], D=60.0, R=30.0)

    def test_invalid_range_in_dp(self) -> None:
        with self.assertRaises(ValueError):
            min_stops_dp([], D=50.0, R=0.0)


if __name__ == "__main__":
    unittest.main()
