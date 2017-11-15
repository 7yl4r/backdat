
def make_plan_line(timestr, src, trg):
    """
    returns string matching the format of a line in backup_plan.tsv

    Parameters:
    ------------
    timestr : str
        ISO8601 string indicating the time of the backup. (column 0)
    src : str
        absolute path to the file we want to back up
    trg : str
        remote target we want to push to 
    """
    # TODO: ? strftime if timestr is actually datetime
    return "\t".join([timestr, src, trg]) + "\n"
