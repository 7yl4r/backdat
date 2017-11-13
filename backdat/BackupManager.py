from datetime import datetime, timedelta
import logging
import platform  # only for platform.node() to get hostname

from croniter import croniter

from backdat.RemoteInterface import rclone
from backdat.file_parsers import backup_plan, host_settings
from backdat.file_parsers import crontab
from backdat.file_parsers import backup_history

# TODO: un-hardcode these
backdat_exe_path = "/opt/backdat/backdat.py"
cronjob_log_path = "/var/opt/backdat/cronjob.log"

class BackupArgs(object):
    """ basically a dict to pass to the backuper... why didn't I just use a dict? """
    source = "/opt/backdat/backdat.py"
    target = "gdrive-ty:/IMARS/backups/test/"
    log = "/var/opt/backdat/backup.log"
    summarylog = "/var/opt/backdat/summary.log"
    rclonelog = None
    window = "24h"
    verbose = 0

class BackupManager(object):
    """ BackupManager manages backing up of files in a backup session """

    def __init__(self):
        self.next_backup_args = BackupArgs()
        self.logger = logging.getLogger(__name__)

    def start_backups(self):
        """
        starts running backups until we are outside of our allotted window
        """
        self.logger.info(" === START === ")
        try:
            hostname = platform.node()
            for next_backup in backup_plan.read(hostname):
                self.set_next_backup(next_backup)

                if (BackupManager.enough_time_remaining()):
                    self.do_next_backup()
                else:
                    self.logger.info("Not within backup window.")
                    break
            else:
                self.logger.warn("Finished all backups with time to spare!")
        # schedule next run of BackupManager in crontab & exit
        finally:
            winend, next_scheduled_time = BackupManager.get_window_edges(
                BackupManager.get_host_setting(host_settings.KEYS.BACKUP_TIMES)
            )

            crontab.write_crontab(next_scheduled_time)

            # TODO: update backup plan before exiting
            self.logger.info(" === END === ")

    def do_next_backup(self):
        """
        do the next backup action
        """
        self.logger.info("starting next backup action...")
        rclone.backup(self.next_backup_args)
        backup_history.log_backup_action(self.next_backup_args)

    def set_next_backup(self, backup_dict):
        """ loads given backup dict into next_backup_args """
        self.next_backup_args.source = backup_dict["source"]
        self.next_backup_args.target = backup_dict["target"]

    @staticmethod
    def get_host_setting(key):
        settings = host_settings.read()
        return settings[key]

    @staticmethod
    def enough_time_remaining():
        """
        return true if we have enough time left in the window to complete
        the next backup task
        """
        estimated_next_backup_tf = datetime.now() + timedelta(minutes=5)  # NOTE: could calc better estimate
        return BackupManager.inside_cron_window(
            estimated_next_backup_tf,
            BackupManager.get_host_setting(host_settings.KEYS.BACKUP_TIMES)
        )

    @staticmethod
    def inside_cron_window(dtime, windowstr):
        """
        returns true if given datetime is within given widow cron string

        ---------
        dtime : datetime
        windowstr : str
        """
        window_end, next_window = BackupManager.get_window_edges(windowstr)
        if dtime < window_end:
            return True
        else:
            return False

    @staticmethod
    def get_window_edges( windowstr):
        """
        return datetime of the end given backup window
        and the datetime of the start of the next window
        """
        # threshold should be << than window width, but > cron granularity
        # this method assumes that the cron string minutes column is *, ie
        # cron granularity is 1min and min window width is 1hr.
        threshold = timedelta(minutes=2)

        last_time = datetime.now()
        window_iter = croniter(windowstr, last_time)
        while(True):
            next_time = window_iter.get_next(datetime)
            if next_time - last_time < threshold:
                last_time = next_time
            else:
                # self.logger.debug("running until " + str(last_time) + ".")
                # self.logger.debug("will resume at " + str(next_time))
                return last_time, next_time
