#!/usr/bin/env python3
"""
tests stats read/write/update
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
from backdat.file_parsers import backup_stats

class Test_statsfile_io(TestCase):
    # example statfile for testing:
    test_statfile_path = "/opt/backdat/docs/example_files/output/backup-stats.json"

    def _get_mock_stats(self):
        return {
            '//': [
                '/var/opt/backdat/backup-stats.json',
                " Shows running stats kept on the current host's backup history."
            ],
            'backdat.actions_completed': 234,
            'backdat.bytes_uploaded': 12345678
        }

    # tests:
    #########################
    def test_read_demo_statfile(self):
        """ read demo statfile """
        result = backup_stats.read(filepath=self.test_statfile_path)
        self.assertEqual(result, self._get_mock_stats())

    def test_read_demo_statfile(self):
        """ read when no statsfile should return zero-d stats """
        fake_statpath = "/i/am/not/a/real/file/path.json"
        result = backup_stats.read(filepath=fake_statpath)
        self.assertEqual(result, backup_stats._get_zero_stats())
