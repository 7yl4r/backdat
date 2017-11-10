from backdat.BackupManager import BackupManager

def backup(args):
    backman = BackupManager()
    backman.start_backups()

def status(args):
    print("status: NYI")
