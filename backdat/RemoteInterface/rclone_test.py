#!/usr/bin/env python3
"""
tests for the rclone driver
"""

# std modules:
from unittest import TestCase
try:
    # py2
    from mock import MagicMock
except ImportError:
    # py3
    from unittest.mock import MagicMock


# dependencies:
from backdat.RemoteInterface import rclone

class Test_rclone_driver(TestCase):
    # tests:
    #########################
    def test_parse_elapsed_time_seconds_only(self):
        """ test parse elapsed on seconds only output """
        result = rclone.parse_time_spent("Elapsed time:  27.9s")
        self.assertEqual(result, 28)
    def test_parse_elapsed_time_min_n_sec(self):
        """ test parse elapsed time min+sec """
        result = rclone.parse_time_spent("Elapsed time:  18m27.9s")
        self.assertEqual(result, 1108)
    def test_parse_elapsed_time_hr_min_sec(self):
        """ test parse elapsed time hr+min+sec """
        result = rclone.parse_time_spent("Elapsed time:  1h18m27.9s")
        self.assertEqual(result, 4708)
