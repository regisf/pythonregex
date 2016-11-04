"""
Test suite for the application

Using the test suite in a shell or console:
    python tests/test.py
"""

__author__ = 'Régis FLORET'

import unittest


class TestEmailModel(unittest):
    def test_get_template(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
