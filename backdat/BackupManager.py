from datetime import datetime, timedelta

from croniter import croniter

from backdat.RemoteInterface import rclone
from backdat import backup_plan_parser
from backdat import host_settings_parser

class mockArgs(object):
    source = "/home/tylar/backdat/backdat.py"
    target = "gdrive-ty:/IMARS/backups/test/"
    log = "/var/opt/backdat/backup.log"
    summarylog = "/var/opt/backdat/summary.log"
    rclonelog = None
    window = "24h"
    verbose = 0

class BackupManager(object):
    """ BackupManager manages backing up of files in a backup session """

    def __init__(self):
        self.next_backup_args = mockArgs()

    def start_backups(self):
        """
        starts running backups until we are outside of our allotted window
        """
        for next_backup in BackupManager.load_backup_plan():
            self.set_next_backup(next_backup)
            if (BackupManager.enough_time_remaining()):
                self.do_next_backup()
            else:
                # TODO: schedule next run of BackupManger in crontab & exit
                return
    def do_next_backup(self):
        """
        do the next backup action
        """
        rclone.backup(self.next_backup_args)

    @staticmethod
    def enough_time_remaining():
        """
        return true if we have enough time left in the window to complete
        the next backup task
        """
        settings = host_settings_parser.read("/etc/opt/backdat/host-settings.cfg")  # TODO: make this cross-platform
        estimated_next_backup_tf = datetime.now() + timedelta(minutes=5)  # TODO: calc better estimate
        return BackupManager.inside_cron_window(
            estimated_next_backup_tf,
            settings[host_settings_parser.KEYS.BACKUP_TIMES]
        )

    @staticmethod
    def inside_cron_window(dtime, windowstr):
        """
        returns true if given datetime is within given widow cron string

        ---------
        dtime : datetime
        windowstr : str
        """
        # threshold should be << than window width, but > cron granularity
        # this method assumes that the cron string minutes column is *, ie
        # cron granularity is 1min and min window width is 1hr.
        threshold = timedelta(minutes=2)

        window_iter = croniter(windowstr, dtime)
        while(True):
            next_time = window_iter.get_next(datetime)
            if next_time < dtime:
                pass  # keep getting times until we pass our target time
            elif next_time - dtime < threshold:
                # if the next time is close to our target time
                return True
            else:
                # if the next time is far off, we probably exited our window
                return False

    def set_next_backup(self, backup_dict):
        """ loads given backup dict into next_backup_args """
        self.next_backup_args.source = backup_dict["source"]
        self.next_backup_args.target = backup_dict["target"]

    @staticmethod
    def load_backup_plan():
        """
        loads backup plan actions for this host from file into a list
        """
        return backup_plan_parser.read(
            "/var/opt/backdat/backup-plan.tsv",  # TODO: make this cross-platform
            "tylardesk"  # TODO: get this dynamically
        )
