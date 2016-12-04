"""
Test suite for the application

Using the test suite in a shell or console:
    python tests/test.py
"""

import unittest


__author__ = u'Régis FLORET'


class TestEmailModel(unittest.TestCase):
    def test_get_template(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
