#!/usr/bin/env python3

""" example main file with cmd line interface """
from argparse import ArgumentParser
import logging

from backdat.main import backup, status, plan

if __name__ == "__main__":
    # === set up arguments
    parser = ArgumentParser(description='declarative backup manager')

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="count",
                        default=0
    )
    parser.set_defaults(func=backup)  # set default behavior if subcommand not given

    subparsers = parser.add_subparsers(
        title='subcommands',
        description='usage: `backdat $subcommand` ',
        help='addtnl help for subcommands: `backdat $subcommand -h`'
    )

    parser_status = subparsers.add_parser('status', help='host coverage assessment')
    # parser_status.add_argument('hostname', type=str, help='name of host to check')
    parser_status.set_defaults(func=status)

    parser_backup = subparsers.add_parser('backup', help='try backing up right now')
    parser_backup.set_defaults(func=backup)

    parser_plan = subparsers.add_parser('plan', help='generate backup plan')
    parser_plan.set_defaults(func=plan)

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

    args.func(args)
