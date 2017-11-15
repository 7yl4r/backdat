"""
basic reading & writing of backup plan files
formatted to match ./docs/example_files/backup-plan.tsv
"""

import logging
import os

PLAN_PATH="/var/opt/backdat/backup-plan.tsv"

def read(hostname, filepath=PLAN_PATH):
    """
    reads in a backup plan from file

    -----------
    hostname : str
        limit returned object to plans for this host only
    """
    logger = logging.getLogger(__file__)
    plan = list()

    with open(filepath, 'r') as planfile:
        for i, line in enumerate(planfile):
            try:
                if line.lstrip().startswith("#"):  # skip comment lines
                    pass
                elif not line.strip():  # skip blank lines
                    pass
                else:
                    datetime, source, target = map(str.strip,
                        line.split("\t")
                    )
                    line_hostname, path = map(str.strip,
                        source.split(":")
                    )
                    if hostname == line_hostname:
                        plan.append({"source": path, "target": target})
            except ValueError as v_err:
                logger.critical("Parse error ({})\n\t@ {} L{} :\n'''\n{}'''\n".format(
                    v_err, filepath, i, line
                ))
    logger.info(str(len(plan)) + " plans read from file")
    return plan

def add_line(plan_line, filepath):
    """ writes a line  to the backup plan
    if a line that is similar enough matches this line, that line is replaced
    """
    # TODO
    return

def remove_completed_action(backup_args):
    """
    removes line from backup plan (because it has been completed)
    """
    line_to_remove = "TODO TODO TODO"
    TMP_PATH=PLAN_PATH+".tmp"
    with open(PLAN_PATH, 'r') as planfile:
        with open(TMP_PATH, 'wb') as tmpfile:
            for line in planfile:
                if line != line_to_remove:
                    tmpfile.write(line)
    os.replace(TMP_PATH, PLAN_PATH)  # new in python v 3.3
