from backdat.RemoteInterface import rclone

class mockArgs(object):
    source = ""
    target = ""
    log = ""
    summarylog = ""
    rclonelog = ""
    window = ""
    verbose = ""

class BackupManager(object):
    """ BackupManager manages backing up of files in a backup session """

    def __init__(self, param):
        """ constructor """
        self.next_backup_args = mockArgs()

    def backup(self):
        rclone.backup(self.next_backup_args)
