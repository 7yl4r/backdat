#!/usr/bin/env python3
"""
tests dotfile loader
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
from backdat import DotfileConfig

class Test_dotfile_config_loader(TestCase):

    # tests:
    #########################
    def test_get_local_config_file_on_example_dir(self):
        """ get_local_config_file using included example .backupconfig """
        src = '/opt/gdrive-backuper/example'
        result = DotfileConfig.get_local_config_file(src)

        self.assertEqual(result, src + '/'+DotfileConfig.CFGNAME)

    def test_get_local_config_file_on_example_file(self):
        """ get_local_config_file using included example .backupconfig dir """
        srcdir = '/opt/gdrive-backuper/example'
        srcfile = '/my-file.txt'
        src = srcdir + srcfile
        result = DotfileConfig.get_local_config_file(src)

        self.assertEqual(result, srcdir + '/'+DotfileConfig.CFGNAME)
