from backdat.RemoteInterface import rclone

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
        for next_backup in self.load_backup_plan():
            self.set_next_backup(next_backup)
            if (self.enough_time_remaining()):
                self.do_next_backup()
            else:
                # TODO: schedule next run of BackupManger in crontab & exit
                return
    def do_next_backup(self):
        """
        do the next backup action
        """
        rclone.backup(self.next_backup_args)

    def enough_time_remaining(self):
        """
        return true if we have enough time left in the window to complete
        the next backup task
        """
        # TODO: load host_settings
        # TODO: if time left in window
        return True

    def set_next_backup(self, backup_dict):
        """ loads given backup dict into next_backup_args """
        self.next_backup_args.source = backup_dict["source"]
        self.next_backup_args.target = backup_dict["target"]

    def load_backup_plan(self):
        """
        loads backup plan actions for this host from file into a list
        """
        # TODO: read this from file
        return [
            {
                'source' : "/home/tylar/backdat/backdat.py",
                'target' : "gdrive-ty:/IMARS/backups/test/"
            },{
                'source' : "/home/tylar/backdat/LICENSE",
                'target' : "gdrive-ty:/IMARS/backups/test/"
            }
        ]
