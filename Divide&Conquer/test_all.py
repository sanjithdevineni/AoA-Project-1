"""Aggregate test module for unittest discovery."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Handle folder name with special characters
ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))


def load_tests(
    loader: unittest.TestLoader,
    tests: unittest.TestSuite,
    pattern: str,
) -> unittest.TestSuite:
    """Load all tests from the tests directory."""
    start_dir = ROOT / "tests"
    return loader.discover(start_dir=str(start_dir), pattern=pattern or "test*.py")


if __name__ == "__main__":
    unittest.main()