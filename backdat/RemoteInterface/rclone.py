# === built-in imports
import argparse
import logging
from logging.handlers import RotatingFileHandler
import subprocess
import sys
import os
import re

# === import dependencies
# NONE (yet...)

# === imports from this package
from backdat.ProcessWrapHandler import ProcessWrapHandler
from backdat.DotfileConfig import DotfileConfig

# === global vars
MY_PATH    = '/var/opt/backdat/'
RCLONE     = "rclone"
RCLONE_CFG = MY_PATH + "rclone.conf"

if not MY_PATH in sys.path:  # TODO: rm this
    sys.path.append(MY_PATH)


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
    logger = logging.getLogger(__file__)
    logger.info('starting backuper...')

    logfile_handler = RotatingFileHandler(
       args.backuper_log, maxBytes=1e6, backupCount=5
    )

    #logfile_handler.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
    rclone_cmd = build_rclone_cmd(args)
    logger.info(str(rclone_cmd))
    try:
        res_stdout = subprocess.check_output(rclone_cmd,
            # stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        # logger.debug(res.args)

    except subprocess.CalledProcessError as sub_err:
        logger.error("rclone subprocess failure; returned "+ str(sub_err.returncode))
        res_stdout = sub_err.output
        raise sub_err

    finally:
        logger.debug("\n############# BEGIN SUBPROCESS OUTPUT #############\n")
        logger.debug(res_stdout)

        # write separate rclonelog if given
        if args.rclonelog is not None:
            with open(args.rclonelog, "a") as rclonelog:
                rclonelog.write(res_stdout)

        logger.debug("\n#############  END SUBPROCESS OUTPUT  #############\n")
        # logger.info('rclone exit w/ code ' + str(res.returncode))

    logger.info('starting post-job hooks...')
    process_handler.post(args.backuper_log)

    # status=`$RCLONE -v --modify-window 672h --config=$CFG sync $CP_FROM $CP_TARGET | tee /dev/fd/5 | tail -200`

    # record metrics in args.summarylog
    def parse_units(number, units):
        """ parses units strings from rclone status """
        number = float(number)
        if (units == "Bytes"):
            return number
        elif(units == "kBytes"):
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
        logger.debug("parsing rclone output: \n" + str(last_status))
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
            '\t"backuper.bytes_sent":' + str(bytes_sent) + ',\n'
            '\t"backuper.avg_speed":' + str(avg_speed) + ',\n'
            '\t"backuper.errors":' + str(err_count) + ',\n'
            '\t"backuper.files_checked":' + str(check_count) + ',\n'
            '\t"backuper.files_sent":' + str(files_sent) + ',\n'
            '\t"backuper.time_spent":' + str(time_spent) + '\n'
            "}\n"
        )
