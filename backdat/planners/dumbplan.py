"""
the dumbest backup plan.
mostly for testing and cases where you have huge over-coverage.
plans on backing up every file within every backup window.
"""
from datetime import datetime
import platform  # only for platform.node() to get hostname

from backdat.file_parsers.fileset import get_fileset_statlist, STAT_KEYS
from backdat.file_parsers import backup_plan

def make_plan():
    with open("/var/opt/backdat/backup-plan.tsv", 'w') as planfile:
        planfile.write(
            "# !!! this backup plan was generated by backdat                  !!!\n" +
            "# !!! any changes made here will likely be ignored & overwritten !!!\n"
        )

        for fstat in get_fileset_statlist():   # for every file in fileset
            # plan to back it up on the next run
            timestr = "2222-22-22T22:22:22"
            hostname = platform.node()
            src = hostname +":" + fstat[STAT_KEYS.SOURCE]

            # the target path is built using the current month for additional
            # backups. You may not want this, so an option to configure it
            # should probably be added.
            month = datetime.today().month
            trg = (
                "gdrive-ty:/IMARS/backups/backdat/" +
                str(month) + "/" +
                hostname + "/"
                # fstat[STAT_KEYS.TARGET]
            )
            planfile.write("\t".join([timestr, src, trg]) + "\n")
