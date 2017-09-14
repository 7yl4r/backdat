# === built-in imports
import argparse
import logging
import subprocess
import sys
import os
import re

# === import dependencies
# NONE (yet...)

# === global vars
MY_PATH    = '/opt/gdrive-backuper/'
RCLONE     = MY_PATH + "rclone/rclone"
RCLONE_CFG = MY_PATH + "rclone.conf"

if not MY_PATH in sys.path:
    sys.path.append(MY_PATH)

# === imports from this package
from gdrive_backup.ProcessWrapHandler import ProcessWrapHandler
from gdrive_backup.DotfileConfig import DotfileConfig

# === logger setup
logger = logging.getLogger('gdrive_backuper')
logger.setLevel(logging.DEBUG)

log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

def build_rclone_cmd(args):
    """
    builds up the command for rclone
    """
    # TODO: set log-level based on args.verbose value
    cmd = [
        RCLONE,
        '--modify-window', args.window,
        '--config', RCLONE_CFG,
        # '--log-file', args.rclonelog,
        '--log-level', 'INFO',
        'sync',
        args.source, args.target
    ]
    return cmd

def backup(args):
    """
    main backup function. performs backup using rclone with additional
    features.
    """
    logger.info('starting backuper...')
    logfile_handler = logging.FileHandler(args.log)
    #logfile_handler.setLevel(logging.DEBUG)
    logfile_handler.setFormatter(log_formatter)
    logger.addHandler(logfile_handler)

    logger.info('checking for dotfiles...')
    process_handler = ProcessWrapHandler(
        DotfileConfig(args.source).config,
        args.source,
        logger
    )

    logger.info('starting pre-job hooks...')
    process_handler.pre()

    logger.info('starting rclone job...')
    res_stdout = subprocess.check_output(build_rclone_cmd(args),
        # stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    # logger.debug(res.args)

    logger.debug("\n############# BEGIN RCLONE OUTPUT #############\n")
    logger.debug(res_stdout)

    # write separate rclonelog if given
    if args.rclonelog is not None:
        with open(args.rclonelog, "a") as rclonelog:
            rclonelog.write(res_stdout)

    logger.debug("\n#############  END RCLONE OUTPUT  #############\n")
    # logger.info('rclone exit w/ code ' + str(res.returncode))

    logger.info('starting post-job hooks...')
    process_handler.post(args.log)

    # status=`$RCLONE -v --modify-window 672h --config=$CFG sync $CP_FROM $CP_TARGET | tee /dev/fd/5 | tail -200`

    # record metrics in args.summarylog
    def parse_units(number, units):
        """ parses units strings from rclone status """
        if (units == "Bytes"):
            return number
        elif(units == "KBytes"):
            return number*1e3
        elif(units == "MBytes"):
            return number*1e6
        elif(units == "GBytes"):
            return number*1e9
        elif(units == "TBytes"):
            return number*1e12
        else:
            raise ValueError("unknown units: ", units)

    with open(args.summarylog, "w") as sumlog:
        # get last status printout from rclone
        last_status = res_stdout.split("\n")[-6:]

        # parse out the various numbers
        byte_num, byte_unit  = last_status[0].split(':')[1].strip().split(' ')[:2]
        bytes_sent = parse_units(byte_num, byte_unit)

        speed_num, speed_unit = last_status[0].split('(')[1].split(')')[0].split(' ')
        avg_speed = parse_units(speed_num, speed_unit[:-2])  # :-2 strips the /s

        err_count  = last_status[1].split(":")[1].strip()
        check_count = last_status[2].split(":")[1].strip()
        files_sent = last_status[3].split(":")[1].strip()

        time_parts = re.findall(r"[-+]?\d*\.\d+|\d+", last_status[4].split(":")[1])
        if (len(time_parts) == 1):  # s only
            time_spent = time_parts[0]
        elif (len(time_parts) == 2):  # m & s
            time_spent = time_parts[0]*60 + time_parts[1]
        elif (len(time_parts) == 3):  # h m s
            time_spent = time_parts[0]*60*60 + time_parts[1]*60 + time_parts
        else:
            raise ValueError("cannot parse time array : " + str(time_parts))

        # write a summary of the rclone output to file
        sumlog.write("{\n" +
            '\t"backuper.bytes_sent":' + bytes_sent + ',\n'
            '\t"backuper.avg_speed":' + avg_speed + ',\n'
            '\t"backuper.errors":' + err_count + ',\n'
            '\t"backuper.files_checked":' + check_count + ',\n'
            '\t"backuper.files_sent":' + files_sent + ',\n'
            '\t"backuper.time_spent":' + time_spent + '\n'
            "}\n"
        )