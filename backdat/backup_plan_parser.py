"""
basic reading & writing of backup plan files in format in this mockup:
https://gist.github.com/7yl4r/291f94c5ca16782e147c346471c36695
"""

def read(filepath, hostname):
    """
    reads in a backup plan from file

    -----------
    hostname : str
        limit returned object to plans for this host only
    """
    plan = list()

    with open(filepath, 'r') as planfile:
        for line in planfile:
            if line.lstrip().startswith("#"):  # skip comment lines
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
    return plan

def write(filepath):
    """ writes a backup plan to file """
    # TODO
    return
