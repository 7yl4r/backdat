from backdat.BackupManager import BackupManager
from backdat.assessments import assessment_report, get_theoretical_assessment
from backdat.planners.dumbplan import make_plan
from backdat.file_parsers.backup_history import get_last_upload_times

def backup(args):
    backman = BackupManager()
    backman.start_backups()

def status(args):
    print(
        assessment_report(
            get_theoretical_assessment()
        )
    )

def plan(args):
    make_plan()

def check(args):
    print("last back up(s): " + str(get_last_upload_times(args.filename, n_times=3)))