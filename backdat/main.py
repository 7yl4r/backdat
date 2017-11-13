from backdat.BackupManager import BackupManager
from backdat.assessments import assessment_report, get_theoretical_assessment
from backdat.planners.dumbplan import make_plan

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
