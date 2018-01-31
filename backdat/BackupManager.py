from datetime import datetime, timedelta
import logging

from croniter import croniter

from backdat.RemoteInterface import rclone
from backdat.file_parsers import backup_plan, host_settings
from backdat.file_parsers import crontab
from backdat.file_parsers import backup_history
from backdat.file_parsers import backup_stats
from backdat.util.get_hostname import get_hostname
from backdat.planners.util import make_plan_line
from backdat.planners.dumbplan import make_plan

class BackupArgs(object):
    """ basically a dict to pass to the back up driver (RemoteInterface)...
    why didn't I just use a dict?
    """
    source = "/opt/backdat/backdat.py"
    target = "gdrive-ty:/IMARS/backups/test/"
    backuper_log = "/var/opt/backdat/backup.log"
    summarylog = "/var/opt/backdat/summary.log"
    rclonelog = None
    window = str(24*30)+"h"
    verbose = 0

    def get_plan_line(self):
        """
        convert BackupManger.BackupArgs object into string matching the
        format of a line in backup_plan.tsv
        """
        time_string = "2222-22-22T22:22:22"  # TODO: somehow use real time here?
        return make_plan_line(time_string, get_hostname() + ":" + self.source, self.target)

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
            hostname = get_hostname()
            for next_backup in backup_plan.read(hostname):
                self.logger.debug(".")
                self.set_next_backup(next_backup)

                if (BackupManager.enough_time_remaining()):
                    self.do_next_backup()
                else:
                    self.logger.info("Not within backup window.")
                    break
            else:
                self.logger.warn("Finished all backups with time to spare!")
                # re-plan?
                make_plan()
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
        try:
            rclone.backup(self.next_backup_args)
            status = backup_stats.ACTION_STATUS.DONE
            backup_history.log_backup_action(self.next_backup_args)
        except Exception as err:
            self.logger.error("backup action failed!", err)
            status = backup_stats.ACTION_STATUS.FAIL
        finally:
            backup_stats.update_stats(
                self.next_backup_args,
                status
            )
            backup_plan.remove_action(self.next_backup_args)

    def set_next_backup(self, backup_dict):
        """ loads given backup dict into next_backup_args """
        self.logger.debug(backup_dict["source"] + "\n\t=> " + backup_dict["target"])
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
        estimated_next_backup_tf = datetime.now() + timedelta(minutes=5)
        # NOTE: could calc better estimate
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
        logger = logging.getLogger(__file__)
        window_end, next_window = BackupManager.get_window_edges(windowstr)
        if dtime < window_end:
            logger.debug(str(dtime) + " is inside the window")
            return True
        else:
            logger.debug(str(dtime) + " is after end of window")
            return False

    @staticmethod
    def get_window_edges( windowstr, MAX_DELTA=timedelta(hours=25)):
        """
        Returns datetime of the end current backup window
        and the datetime of the start of the next window.
        Assumes the window is smaller than MAX_DELTA.

        Parameters
        ----------------
        windowstr : crontab-like str
            the window to explore
        MAX_DELTA : datetime.timedelta
            max time in future to check for the window before giving up
            and assuming the window is infinite
        """
        logger = logging.getLogger(__file__)
        def _max_window_edges():
            """ use this when the window looks infinite """
            return datetime.max, datetime.now() + timedelta(hours=1)

        if windowstr == "* * * * *":
            logger.warn("Attempting to calculate edge of infinite window!")
            return _max_window_edges()
        else:
            time_to_give_up = datetime.now() + MAX_DELTA
            last_time = datetime.now()
            # threshold should be << than window width, but > cron granularity
            # this method assumes that the cron string minutes column is *, ie
            # cron granularity is 1min and min window width is 1hr.
            threshold = timedelta(minutes=2)
            window_iter = croniter(windowstr, last_time)
            while(True):
                next_time = window_iter.get_next(datetime)
                if next_time - last_time < threshold:
                    # logger.debug(
                    #     'next:' + str(next_time) +
                    #     ' last:' + str(last_time)
                    # )
                    if last_time > time_to_give_up:
                        logger.warn(
                            "Search for end of window exceeded MAX_DELTA (" +
                            str(MAX_DELTA) + ")"
                        )
                        return _max_window_edges()
                    else:
                        last_time = next_time
                else:
                    logger.debug("running until  " + str(last_time))
                    logger.debug("will resume at " + str(next_time))
                    return last_time, next_time
