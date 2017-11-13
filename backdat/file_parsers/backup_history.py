"""
This user-facing file is a history of items that have been backed up.
"""

from datetime import datetime

DEFAULT_PATH = "/var/opt/backdat/backup-history.log"

def log_backup_action(action, logpath=DEFAULT_PATH):
    """
    creates log in entry file for given action

    Parameters
    ----------
    action : BackupManager.BackupArgs
        backup action we just completed that we want to log
    """
    current_time = datetime.now()
    with open(logpath, 'a') as logfile:
        logfile.write("\t".join([
            str(current_time),
            action.source,
            action.target + "\n"
        ]))

def get_last_upload_time(filename, logpath=DEFAULT_PATH):
    """
    returns the last time given filename was uploaded,
    assumes backup file has cronological entries.
    assumes we can fit the whole backup log into memory.
    """
    with open(logpath, 'r') as logfile:
        for line in reversed(list(logfile.readlines())):
            time, src, path = line.split("\t")
            if src == filename:
                return time
        else:
            # file has never been backed up, return the dawn of time
            return str(datetime.min)
