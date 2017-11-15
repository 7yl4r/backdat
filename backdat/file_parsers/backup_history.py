"""
This user-facing file is a history of items that have been backed up.
"""

from datetime import datetime
import logging

from backdat.file_parsers.fileset import get_fileset_statlist, STAT_KEYS

DEFAULT_PATH = "/var/opt/backdat/backup-history.log"
TIME_FORMAT = "%Y-%m-%d %H:%M"

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
            current_time.strftime(TIME_FORMAT),
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
        last_backup = datetime.strptime(
            get_last_upload_times(fstat[STAT_KEYS.SOURCE], n_times=1)[0],
            TIME_FORMAT
        )
        if last_backup < oldest_date:
            oldest_date = last_backup
            oldest_name = fstat[STAT_KEYS.SOURCE]
    return oldest_name, oldest_date

def get_dawn_of_time():
    """
    returns the earliest possible time we can handle as formatted string.

    NOTE: We're not using datetime.min directly because strptime doesn't like
    years shorter than 4 digits and datetime.min.year == 1 :
        # tested in python 3.4:
        >>> datetime.strptime(datetime.strftime(datetime.min, TIME_FORMAT), TIME_FORMAT)
        ValueError: time data '1-01-01 00:00' does not match format '%Y-%m-%d %H:%M'
    """
    return datetime.strftime(datetime.min.replace(year=1000), TIME_FORMAT)

def get_last_upload_times(filename, n_times=1, logpath=DEFAULT_PATH):
    """
    returns list of the last n_times backups
    assumes backup file has cronological entries.
    assumes we can fit the whole backup log into memory.
    """
    logger = logging.getLogger(__name__)
    try:
        times = []
        with open(logpath, 'r') as logfile:
            for line in reversed(list(logfile.readlines())):
                time, src, path = line.split("\t")
                if src == filename:
                    times.append(time)
                    if len(times) == n_times:
                        break
            else:
                logger.warn("not enough backups in history for: " + filename)
        logger.debug("found " + str(len(times)) + " past backups for " + filename)
        while len(times) < n_times:
            # append dawn of time for non-existent entries
            times.append(get_dawn_of_time())
        return times
    except FileNotFoundError as f_err:
        logger.warn("No backup history found")
        return [get_dawn_of_time()]*n_times

def get_backup_frequency(n_backups_to_check):
    """
    checks for repeated backups in history and calculates frequency using at
    most the last n_backups_to_check.
    """
    # TODO: for each file (or maybe just a few of them to save time)
    # TODO: get a list of the last backup times
    # TODO: calculate avg frequency of backups using last n_backups_to_check
