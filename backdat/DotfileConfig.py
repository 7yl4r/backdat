#!/usr/bin/env python3
"""
configuration as specified by dotfiles (system and local), similar to git
"""

import os
import json

CFGNAME = '.backdatconfig'

# logger = logging.getLogger('gdrive_backuper.dotfileconfig')
# logger.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# logger.addHandler(console_handler)


def get_local_config_file(local_location):
    """
    returns path of config file for given location path if exists.
    throws exception if no config found.

    if local_location is a dir: looks in that dir
    if local_location is file: looks in file's parent dir
    """

    if os.path.isdir(local_location):
        parent = local_location
        files = os.listdir(local_location)
    else:
        parent = os.path.dirname(local_location)
        files = os.listdir(parent)

    if CFGNAME in files:
        return os.path.join(parent, CFGNAME)
    else:
        raise AssertionError('no config file found.')

class DotfileConfig(object):
    def __init__(self, location, globalconfig=None):
        """
        location : location we are talking about
        globalconfig : global config file for fallback values
        """
        if globalconfig is None:
            # TODO: get global config from expected dir
            pass
        else:
            raise NotImplementedError('NYI')

        self._init_config()

        # TODO: load global config and then overload w/ local
        #       for now we ignore global config
        #self.load_config(global_config_file)

        try:
            local_config_path = get_local_config_file(location)
            self.load_config(local_config_path)

        except AssertionError:
            # no local config found, just return global
            pass

        return

    def _init_config(self):
        self.config = {
            "pre": [],
            "post": [],
            "on_error": []
        }

    def load_config(self, config_file_path):
        """
        loads a config from the given file path
        """
        with open(config_file_path) as data_file:
            data = json.load(data_file)
            for key in self.config:  # for pre, post, on_error, etc
                try:
                    self.config[key].extend(data[key])  # copy over new entries
                except KeyError as k_err:
                    print('no key' + key + 'in cfg file. skipping.', k_err)
