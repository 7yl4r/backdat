"""
parse host settings file based on mockup at:
https://gist.github.com/7yl4r/291f94c5ca16782e147c346471c36695
"""

class KEYS(object):
    BACKUP_TIMES="backup_times"

def read(filepath):
    settings = dict()
    with open(filepath, 'r') as settingsfile:
        for line in settingsfile:
            if line.lstrip().startswith("#"):  # skip comment lines
                pass
            elif not "=" in line:  # skip lines without "="
                pass
            else:
                key, val = map(str.strip, line.split("="))
                if key == KEYS.BACKUP_TIMES:
                    # TODO: validate cron string
                    settings[KEYS.BACKUP_TIMES] = val
                else:
                    raise ValueError(
                        "unknown key in host settings: '{}'".format(key)
                    )
    return settings