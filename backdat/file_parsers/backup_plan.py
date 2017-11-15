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

def trim_time_column(line):
    """
    trims the time column off the front of the given line from backup plan file.
    Useful when you're searching for a particular backup plan entry but don't care
    about the time.
    """
    return " ".join(line.split("\t")[1:])

def remove_completed_action(backup_args):
    """
    Removes line from backup plan (because it has been completed).
    Ignores the time of the planned action.
    """
    logger = logging.getLogger(__file__)
    line_to_remove = backup_args.get_plan_line()
    trimmed_line_to_remove = trim_time_column(line_to_remove)
    TMP_PATH=PLAN_PATH+".tmp"
    lines_found = 0
    with open(PLAN_PATH, 'r') as planfile:
        with open(TMP_PATH, 'w') as tmpfile:
            for line in planfile:
                if trim_time_column(line) != trimmed_line_to_remove:
                    tmpfile.write(line)
                else:
                    lines_found += 1
    # error checking
    if lines_found == 1:
        logger.debug("action removed from plan: " + trimmed_line_to_remove)
    elif lines_found == 0:
        logger.error("plan action not found: " + trimmed_line_to_remove)
    else:
        logger.error("multiple plan actions matching: " + trimmed_line_to_remove)

    # overwrite with tmpfile
    os.replace(TMP_PATH, PLAN_PATH)  # new in python v 3.3
