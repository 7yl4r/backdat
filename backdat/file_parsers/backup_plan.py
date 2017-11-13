"""
basic reading & writing of backup plan files
formatted to match ./docs/example_files/backup-plan.tsv
"""

import warnings

PLAN_PATH="/var/opt/backdat/backup-plan.tsv"

def read(hostname, filepath=PLAN_PATH):
    """
    reads in a backup plan from file

    -----------
    hostname : str
        limit returned object to plans for this host only
    """
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
                warnings.warn("\nWARN: Parse error ({})\n\t@ {} L{} :\n'''\n{}'''\n".format(
                    v_err, filepath, i, line
                ))
    return plan

def add_line(plan_line, filepath):
    """ writes a line  to the backup plan
    if a line that is similar enough matches this line, that line is replaced
    """
    # TODO
    return
