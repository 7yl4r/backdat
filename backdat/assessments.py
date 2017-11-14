import logging
from datetime import datetime, timedelta

from croniter import croniter

from backdat.file_parsers import host_settings
from backdat.file_parsers import fileset
from backdat.file_parsers import crontab
from backdat.file_parsers import backup_history

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
    throughput_needed = fileset.get_upload_size()
    throughput_needed /= 1.0e6  # b * 1Mb / 1,000,000b  (convert bits to Mbits)

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
        'throughput_demand': throughput_needed,
        'assessment_timedelta': assess_window,
        'throughput_supply': est_throughput,
        'coverage': est_throughput / throughput_needed
    }

def assessment_report(assment):
    """
    return nicely formated report of given assessment
    """
    stalest_file, stalest_date = backup_history.get_most_stale_file()
    return (
        "\n"+
        "=== Backup History ===\n"
        "\tmost stale file: {} - {}\n".format(stalest_date.strftime(backup_history.TIME_FORMAT), stalest_file) +
        "=== Estimated Throughput Analysis ===\n"
        "\t{} / {} Tb throughput used over {}\n".format(
            round(assment['throughput_demand']/1e6),
            round(assment['throughput_supply']/1e6),
            assment['assessment_timedelta']
        ) +
        "\tcoverage: {}%".format(round(assment['coverage']*100.0)) +
        "\n"+
        "=== Backup Scheduling ===\n" +
        "\t" + crontab.get_next_cron_report() +
        "\n"
    )
