#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
mblog
~~~~

This module contains logging functions for GrantsBot/matching. These can log
errors and run history to text files.
"""

import logging
import logging.handlers
import sys
import os


def logrun(filepath, run_time, edited_pages=False, wrote_db=False, logged_errors=False):
    """Log information for each run to external log files.

    Parameters:
        run_time        :   Time that the script starts running
        edited_pages    :   True if any pages were edited
        wrote_db        :   True if the DB was modified at least once
        logged_errors   :   True if any errors were logged

    Example output in log file:
        INFO    2015-01-01 01:00:45.650401      Edited: False   Wrote DB: False Errors: False

    Rotating logs will each be used for 30 d. Two backup logs are kept.
    """

    logpath = os.path.join(filepath, 'log')

    message = '{0}\tEdited: {1}\tWrote DB: {2}\tErrors: {3}'.format(
        run_time, edited_pages, wrote_db, logged_errors)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s\t%(message)s')
    handler = logging.handlers.TimedRotatingFileHandler(
        os.path.join(logpath, 'matching.log'), when='D', interval=30,
        backupCount=2, utc=True)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info(message)


# TODO: add some sort of automatic error notification, possibly
# a post on a wikipage
def logerror(message, filepath, exc_info=False):
    """Log information when an error occurs to an external log file.
    """

    logpath = os.path.join(filepath, 'log')

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(os.path.join(logpath, 'matching_errors.log'))
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.error(message, exc_info=exc_info)
