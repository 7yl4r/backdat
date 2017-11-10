import logging

from backdat import host_settings_parser


def get_theoretical_assessment():
    """
    returns assessment based on theoretical predictions using
    estimated speed of connections between hosts and filesizes.
    """
    return {
        'coverage': 0
    }

def assessment_report(assment):
    """
    return nicely formated report of given assessment
    """
    return (
        "\tCOVERAGE REPORTING NOT YET IMPLEMENTED\n"
        "\tcoverage: {}".format(assment['coverage'])
    )
