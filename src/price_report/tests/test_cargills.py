"""Tests for price_report."""

import unittest

from price_report import cargills


class TestCase(unittest.TestCase):
    """Tests."""

    def test_parse_unit(self):
        """Test."""
        self.assertEqual(
            ('g', 1203.0),
            cargills._parse_unit('1203 g'),
        )


if __name__ == '__main__':
    unittest.main()
