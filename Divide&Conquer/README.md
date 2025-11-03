# Divide-and-Conquer Maximum Subarray

This module implements the divide-and-conquer half of the Analysis of Algorithms project: find the contiguous time period with the maximum total profit for a business given daily profit/loss data.

## Problem Statement

**Real-world problem:** A business records daily profits and losses. Management wants to identify the single contiguous period (e.g., consecutive days) that yielded the highest total profit. This helps identify successful operational periods and inform strategic decisions.

**Abstract problem:** Given an array of real numbers representing daily profits (positive) and losses (negative), find the contiguous subarray with the maximum sum.

## Algorithms Implemented

1. **Divide-and-Conquer (O(n log n))**: Recursively splits the array and checks three cases:
   - Maximum subarray entirely in left half
   - Maximum subarray entirely in right half  
   - Maximum subarray crossing the midpoint

2. **Kadane's Algorithm (O(n))**: Optimal linear-time algorithm using dynamic programming principles

3. **Naive Baseline (O(n²))**: Brute-force enumeration of all possible subarrays for validation

## Setup

- Requires Python >= 3.10
- Dependency: matplotlib (install via `pip install -r "Divide&Conquer/requirements.txt"`)

## Quickstart

```bash
# All commands run from project root (AOA-PROJECT-1/)

# Run tests
python -m unittest discover -s "Divide&Conquer/tests"

# Generate benchmarks
python "Divide&Conquer/benchmark.py"

# Export appendix assets for LaTeX
python "Divide&Conquer/export_appendix.py"

# Run on sample data
python "Divide&Conquer/max_subarray_dc.py" --values="-2,1,-3,4,-1,2,1,-5,4"

python "Divide&Conquer/max_subarray_dc.py" --values="-2,1,-3,4,-1,2,1,-5,4" --use-kadane
```

## Output Structure

- `Divide&Conquer/figures/` - Runtime plots (PNG and PDF)
- `Divide&Conquer/results/` - CSV files with benchmark data
- `Divide&Conquer/appendix/` - LaTeX-ready code listings, figures, and tables

## LaTeX Integration

To include the appendix assets in your LaTeX document:

```latex
\input{Divide&Conquer/appendix/code_max_subarray_dc.tex}
\input{Divide&Conquer/appendix/code_naive_baseline.tex}
\input{Divide&Conquer/appendix/code_benchmark.tex}
\input{Divide&Conquer/appendix/figs.tex}
\input{Divide&Conquer/appendix/tables.tex}
```

## Algorithm Complexity

| Algorithm | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Divide-and-Conquer | O(n log n) | O(log n) |
| Kadane's | O(n) | O(1) |
| Naive | O(n²) | O(1) |

## Example Usage

```python
# Add parent directory to path if needed
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from max_subarray_dc import max_subarray

# Daily profit/loss data
values = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

# Find best profit window
start, end, total = max_subarray(values, use_dc=True)
print(f"Best period: day {start} to day {end}")
print(f"Total profit: ${total:.2f}")
# Output: Best period: day 3 to day 6, Total profit: $6.00
```

## Testing

The test suite includes:
- Unit tests for edge cases (empty arrays, single elements, all negative/positive)
- Cross-validation between D&C, Kadane's, and naive algorithms
- Randomized testing with 50+ test cases
- Boundary condition tests

Run tests with: `python -m unittest discover -s "Divide&Conquer/tests"`
