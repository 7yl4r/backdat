#!/usr/bin/env python3

""" example main file with cmd line interface """
from argparse import ArgumentParser
import logging

from backdat.BackupManager import BackupManager

if __name__ == "__main__":
    # === set up arguments
    parser = ArgumentParser(description='declarative backup manager')

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="count",
                        default=0
    )

    args = parser.parse_args()

    # === set up logging behavior
    if (args.verbose == 0):
        logging.basicConfig(level=logging.WARNING)
    elif (args.verbose == 1):
        logging.basicConfig(level=logging.INFO)
    else: #} (args.verbose == 2){
        logging.basicConfig(level=logging.DEBUG)

    # # (optional) create a file handler
    # handler = logging.FileHandler('hello.log')
    # handler.setLevel(logging.INFO)
    #
    # # (optional) create a custom logging format
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    #
    # # (optional) add the handlers (if any) to the logger
    # logger.addHandler(handler)

    # === call your project's main function
    backman = BackupManager()
    backman.start_backups()
