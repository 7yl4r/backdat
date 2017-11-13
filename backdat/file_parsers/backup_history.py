"""
This user-facing file is a history of items that have been backed up.
"""

from datetime import datetime

from backdat.file_parsers.fileset import get_fileset_statlist, STAT_KEYS

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

def get_most_stale_file(logpath=DEFAULT_PATH):
    """
    returns the filename of the file in the fileset that was least recently backed up
    and the time of the last backup
    """
    oldest_name = ""
    oldest_date = datetime.max
    for fstat in get_fileset_statlist():
        last_backup = datetime.strptime(get_last_upload_time(fstat[STAT_KEYS.SOURCE]), "%Y-%m-%d %H:%M:%S.%f")
        if last_backup < oldest_date:
            oldest_date = last_backup
            oldest_name = fstat[STAT_KEYS.SOURCE]
    return oldest_name, oldest_date

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
