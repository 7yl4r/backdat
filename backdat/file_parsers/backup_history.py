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
            action.target,
            "\n"
        ]))
