"""Unit tests for the divide-and-conquer maximum subarray algorithms."""

from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

# Add parent directory to path to handle folder name with special characters
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from max_subarray_dc import max_subarray, max_subarray_dc, _kadane
from naive_baseline import max_subarray_naive


class TestMaxSubarray(unittest.TestCase):
    def test_classic_example(self) -> None:
        """Test the classic maximum subarray example."""
        values = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
        start, end, total = max_subarray_dc(values, 0, len(values) - 1)
        self.assertEqual(start, 3)
        self.assertEqual(end, 6)
        self.assertAlmostEqual(total, 6.0)

    def test_all_positive(self) -> None:
        """Test with all positive values - should return entire array."""
        values = [1, 2, 3, 4, 5]
        start, end, total = max_subarray_dc(values, 0, len(values) - 1)
        self.assertEqual(start, 0)
        self.assertEqual(end, 4)
        self.assertAlmostEqual(total, 15.0)

    def test_all_negative(self) -> None:
        """Test with all negative values - should return least negative."""
        values = [-5, -2, -8, -1, -4]
        start, end, total = max_subarray_dc(values, 0, len(values) - 1)
        self.assertEqual(start, 3)
        self.assertEqual(end, 3)
        self.assertAlmostEqual(total, -1.0)

    def test_single_element(self) -> None:
        """Test with single element."""
        values = [42.0]
        start, end, total = max_subarray_dc(values, 0, 0)
        self.assertEqual(start, 0)
        self.assertEqual(end, 0)
        self.assertAlmostEqual(total, 42.0)

    def test_empty_array(self) -> None:
        """Test with empty array."""
        values = []
        start, end, total = max_subarray(values)
        self.assertEqual(start, -1)
        self.assertEqual(end, -1)
        self.assertAlmostEqual(total, 0.0)

    def test_two_elements_positive(self) -> None:
        """Test with two positive elements."""
        values = [3.0, 5.0]
        start, end, total = max_subarray_dc(values, 0, 1)
        self.assertEqual(start, 0)
        self.assertEqual(end, 1)
        self.assertAlmostEqual(total, 8.0)

    def test_two_elements_mixed(self) -> None:
        """Test with one positive, one negative."""
        values = [5.0, -3.0]
        start, end, total = max_subarray_dc(values, 0, 1)
        self.assertEqual(start, 0)
        self.assertEqual(end, 0)
        self.assertAlmostEqual(total, 5.0)

    def test_alternating_signs(self) -> None:
        """Test with alternating positive and negative values."""
        values = [5, -2, 3, -1, 4, -3, 2]
        start, end, total = max_subarray_dc(values, 0, len(values) - 1)
        # Maximum is [5, -2, 3, -1, 4] = 9
        self.assertEqual(start, 0)
        self.assertEqual(end, 4)
        self.assertAlmostEqual(total, 9.0)

    def test_dc_vs_kadane(self) -> None:
        """Verify D&C matches Kadane's algorithm on random data."""
        rng = random.Random(42)
        for trial in range(20):
            with self.subTest(trial=trial):
                n = rng.randint(1, 100)
                values = [rng.uniform(-50.0, 50.0) for _ in range(n)]

                dc_start, dc_end, dc_sum = max_subarray_dc(values, 0, n - 1)
                kadane_start, kadane_end, kadane_sum = _kadane(values)

                # Both should find the same maximum sum
                self.assertAlmostEqual(dc_sum, kadane_sum, places=6)

    def test_dc_vs_naive(self) -> None:
        """Verify D&C matches naive algorithm on random data."""
        rng = random.Random(123)
        for trial in range(20):
            with self.subTest(trial=trial):
                n = rng.randint(1, 50)
                values = [rng.uniform(-30.0, 30.0) for _ in range(n)]

                dc_start, dc_end, dc_sum = max_subarray_dc(values, 0, n - 1)
                naive_start, naive_end, naive_sum = max_subarray_naive(values)

                # All three metrics should match
                self.assertEqual(dc_start, naive_start)
                self.assertEqual(dc_end, naive_end)
                self.assertAlmostEqual(dc_sum, naive_sum, places=6)

    def test_kadane_vs_naive(self) -> None:
        """Verify Kadane matches naive algorithm."""
        rng = random.Random(456)
        for trial in range(15):
            with self.subTest(trial=trial):
                n = rng.randint(1, 40)
                values = [rng.uniform(-20.0, 20.0) for _ in range(n)]

                kadane_start, kadane_end, kadane_sum = _kadane(values)
                naive_start, naive_end, naive_sum = max_subarray_naive(values)

                self.assertAlmostEqual(kadane_sum, naive_sum, places=6)

    def test_maximum_at_boundaries(self) -> None:
        """Test when maximum subarray is at array boundaries."""
        # Maximum at start
        values = [10, 5, -20, 1, 1, 1]
        start, end, total = max_subarray_dc(values, 0, len(values) - 1)
        self.assertEqual(start, 0)
        self.assertEqual(end, 1)
        self.assertAlmostEqual(total, 15.0)

        # Maximum at end
        values = [1, 1, -20, 10, 5]
        start, end, total = max_subarray_dc(values, 0, len(values) - 1)
        self.assertEqual(start, 3)
        self.assertEqual(end, 4)
        self.assertAlmostEqual(total, 15.0)

    def test_crossing_maximum(self) -> None:
        """Test when maximum crosses the midpoint."""
        values = [2, -1, 3, -2, 4]
        start, end, total = max_subarray_dc(values, 0, len(values) - 1)
        # Maximum is entire array: 2-1+3-2+4 = 6
        self.assertEqual(start, 0)
        self.assertEqual(end, 4)
        self.assertAlmostEqual(total, 6.0)

    def test_large_values(self) -> None:
        """Test with large profit values."""
        values = [1000, -500, 2000, -100, 1500]
        start, end, total = max_subarray_dc(values, 0, len(values) - 1)
        self.assertEqual(start, 0)
        self.assertEqual(end, 4)
        self.assertAlmostEqual(total, 3900.0)

    def test_precision_with_floats(self) -> None:
        """Test floating-point precision."""
        values = [1.5, -0.5, 2.3, -1.1, 0.8]
        start, end, total = max_subarray_dc(values, 0, len(values) - 1)
        # Maximum subarray is [1.5, -0.5, 2.3] = 3.3
        # Not the entire array because -1.1 + 0.8 = -0.3 (negative)
        self.assertEqual(start, 0)
        self.assertEqual(end, 2)
        self.assertAlmostEqual(total, 3.3, places=10)


if __name__ == "__main__":
    unittest.main()