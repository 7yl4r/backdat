#!/usr/bin/env python3

""" example main file with cmd line interface """
from argparse import ArgumentParser
import logging
from logging.handlers import RotatingFileHandler

from backdat.main import backup, status, plan, check
from backdat.DuplicateLogFilter import DuplicateLogFilter

if __name__ == "__main__":
    # =========================================================================
    # === set up arguments
    # =========================================================================
    parser = ArgumentParser(description='declarative backup manager')

    parser.add_argument(
        "-v", "--verbose",
        help="increase output verbosity",
        action="count",
        default=0
    )

    # set default behavior if subcommand not given
    parser.set_defaults(func=backup)

    subparsers = parser.add_subparsers(
        title='subcommands',
        description='usage: `backdat $subcommand` ',
        help='addtnl help for subcommands: `backdat $subcommand -h`'
    )

    parser_status = subparsers.add_parser(
        'status', help='host coverage assessment'
    )
    # parser_status.add_argument('hostname', type=str, help='host to check')
    parser_status.add_argument(
        '--max_period',
        help='prints max backup period in seconds out of all files & exits',
        action='store_true',
        default=False
    )
    parser_status.set_defaults(func=status)

    parser_backup = subparsers.add_parser(
        'backup', help='try backing up right now'
    )
    parser_backup.set_defaults(func=backup)

    parser_plan = subparsers.add_parser('plan', help='generate backup plan')
    parser_plan.set_defaults(func=plan)

    parser_check = subparsers.add_parser(
        'check', help='show last upload of a specific file'
    )
    parser_check.add_argument(
        'filename', type=str, help='name of the file to check'
    )
    parser_check.set_defaults(func=check)

    args = parser.parse_args()
    # =========================================================================
    # === set up default logging behavior
    # =========================================================================
    # === convert -v, -vv, -vvv, etc into logging levels
    if (args.verbose == 0):
        _level = logging.WARNING
    elif (args.verbose == 1):
        _level = logging.INFO
    else:  # } (args.verbose == 2){
        _level = logging.DEBUG

    # === (optional) create custom logging format(s)
    # https://docs.python.org/3/library/logging.html#logrecord-attributes
    formatter = logging.Formatter(
       '%(asctime)s|%(levelname)s\t|%(filename)s:%(lineno)s\t|%(message)s'
    )

    # === (optional) create handlers
    # https://docs.python.org/3/howto/logging.html#useful-handlers
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(_level)
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(DuplicateLogFilter())

    file_handler = RotatingFileHandler(
       '/var/opt/backdat/backdat.log', maxBytes=1e6, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(DuplicateLogFilter())

    # === add the handlers (if any) to the logger
    _handlers = [
        stream_handler,
        file_handler
    ]

    logging.basicConfig(
        handlers=_handlers,
        level=logging.DEBUG  # must be set to lowest of all levels in handlers
    )
    # =========================================================================

    # call the appropriate subcommand function
    args.func(args)
