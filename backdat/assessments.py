import logging
from datetime import datetime, timedelta

from croniter import croniter

from backdat.file_parsers import host_settings

def get_theoretical_assessment(
    assess_window=timedelta(days=30)
):
    """
    returns assessment based on theoretical predictions using
    estimated speed of connections between hosts and filesizes.

    Parameters:
    ---------------
    assess_timedelta : datetime.timedelta
        assessment based on times between now and now + assess_timedelta
    """
    t_0 = datetime.now()
    t_f = datetime.now() + assess_window

    logger = logging.getLogger(__name__)
    logger.debug("theoretical assessement for window " + str(t_0) + " / " + str(t_f))

    logger.debug("estimating amount of data we need to push over given window...")
    # TODO: read file stat history db for these values:
    throughput_needed = 1000.0  # est Mb needed in given assess_window

    logger.debug("estimating upload speed...")
    # TODO: read resources.json (or history?) for these values:
    upload_speed_Mbps = 8.0  # Mb / s
    upload_speed_Mbpmin = upload_speed_Mbps*60.0  # Mb/s * 60s/min

    logger.debug("estimating throughput over given window...")
    # get the amount of time we have per assess_window
    host_sett = host_settings.read()
    cron_iterator = croniter(
        host_sett[host_settings.KEYS.BACKUP_TIMES],
        t_0
    )
    minutes = 0
    while cron_iterator.get_next(datetime) < t_f :
        minutes += 1

    est_throughput = minutes * upload_speed_Mbpmin  # min * Mb / min = Mb

    return {
        'coverage': est_throughput / throughput_needed
    }

def assessment_report(assment):
    """
    return nicely formated report of given assessment
    """
    return (
        "\tcoverage: {}%".format(round(assment['coverage'])*100)
    )
