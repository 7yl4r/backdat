"""
helpers for reading/writing to fileset.tsv like the example in
`./docs/example_files/fileset.tsv`
"""

import csv
import os
from datetime import timedelta
import logging
# import pprint # needed for debugging only

default_fileset_path="/etc/opt/backdat/fileset.tsv"
class STAT_KEYS:
    SIZE = 'size'
    SOURCE = 'filepath'
    TARGET = 'target'
    UPLOAD_TIME = 'ul_time'

def get_upload_size(fileset_path=default_fileset_path):
    """
    returns:
        total size of all uploads in this host's fileset.tsv
    """
    logger = logging.getLogger(__name__)
    logger.debug("=== file stats ===")
    total_size = 0
    for fstat in get_fileset_statlist(fileset_path):
        logger.debug("{} : {}b".format(fstat[STAT_KEYS.SOURCE].split('/')[-1], fstat[STAT_KEYS.SIZE]))
        total_size += fstat[STAT_KEYS.SIZE]
    logger.debug("=== ==== ===== ===")
    return total_size

def get_fileset_statlist(cfgfilename=default_fileset_path):
    """
    reads given fileset.tsv and outputs list of stats for the files in the
    following form:
    [
        {
            filepath: "/home/me/example_file.txt",
            target: "gdrive-me:/example/remote/target/dir/"
            size: 1024,
            ul_time: 300
        }, {...}, {...}
    ]
    """
    statlist = []
    with open(cfgfilename,'r') as tsvin:
        reader = csv.reader(tsvin, delimiter='\t')
        for row in reader:
            if len(row) < 1 or row[0].startswith('#'): # ignore comment lines
                pass
            else:
                src_filepath = row[0].strip()
                file_paths = []  # List which will store all of the filepaths.
                if "*" in src_filepath:
                    src_filepath = src_filepath.replace("*", "")
                    # Walk the tree.
                    for root, directories, files in os.walk(src_filepath):
                        for filename in files:
                            # Join the two strings to form the full filepath.
                            filepath = os.path.join(root, filename)
                            file_paths.append(filepath)  # Add it to the list.
                elif os.path.isdir(src_filepath):
                    # dir we want to upload all at once
                    file_paths = [src_filepath]
                    if file_paths[-1] != '/':  # assert last char is '/'
                        file_paths += '/'
                else:  # is file
                    file_paths = [src_filepath]

                for src_filename in file_paths:
                    target_dirmap = row[1].strip()
                    # stat file(s)
                    size = os.stat(src_filename).st_size  # in Bytes [B]
                    # estimate upload time
                    # TODO: make estimate here?
                    # float(size)/ul_speed
                    # setup_time = 120  # [s]
                    # ul_est = timedelta(seconds=(ul_time + setup_time))
                    ul_est = None
                    statlist.append({
                        STAT_KEYS.SOURCE: src_filename,
                        STAT_KEYS.TARGET: target_dirmap,
                        STAT_KEYS.SIZE: size,
                        STAT_KEYS.UPLOAD_TIME: ul_est
                    })

    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(statlist)
    return statlist
