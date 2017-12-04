import os
import json
import logging

DEFAULT_STATS_PATH="/var/opt/backdat/backup-stats.json"

class KEYS:
    BYTES_UPLOADED='backdat.bytes_uploaded'
    ACTIONS_COMPLETED='backdat.actions_completed'

def update_stats(completed_action, filepath=DEFAULT_STATS_PATH):
    """
    updates stats file with info from given action.

    -----------
    completed_action : BackupManager.BackupArgs
        backup action that was just completed
    """
    stats = read()
    stats[KEYS.ACTIONS_COMPLETED] += 1
    # NOTE: this does not account for files that were only checked and not
    # actually uploaded. Thus `uploaded_bytes` is probably larger than actual throughput.
    stats[KEYS.BYTES_UPLOADED] += os.stat(completed_action.source).st_size
    write(stats)

def read(filepath=DEFAULT_STATS_PATH):
    """ reads in the stats """
    logger = logging.getLogger(__name__)
    try:
        with open(filepath, 'r') as statsfile:
            return json.load(statsfile)
    except FileNotFoundError as f_err:
        logger.warn("backup_stats file does not exist, returning zeroed stats.")
        return _get_zero_stats()

def write(data_dict, filepath=DEFAULT_STATS_PATH):
    """ writes given data_dict to statsfile """
    with open(filepath, 'w') as statsfile:
        json.dump(data_dict, statsfile)

def _get_zero_stats():
    """ returns a stats dict with all stats zeroed out """
    return {
        KEYS.BYTES_UPLOADED: 0,
        KEYS.ACTIONS_COMPLETED: 0
    }
