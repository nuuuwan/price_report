"""Tests for price_report."""

import unittest

from price_report import run_price_report


class TestCase(unittest.TestCase):
    """Tests."""

    def test_run_price_report(self):
        """Test."""
        self.assertTrue(run_price_report.run_price_report())


if __name__ == '__main__':
    unittest.main()
