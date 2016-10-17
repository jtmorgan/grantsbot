#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
utils
=====

Utility functions for matching.py.
"""


import datetime
import json
import os


#testme
def parse_timestamp(t):
    """Parse MediaWiki-style timestamps and return a datetime."""
    if t == '0000-00-00T00:00:00Z':
        return None
    else:
        return datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ')


def load_config(filepath):
    """Given the path to the config file, opens and returns the dict."""
    configfile = os.path.join(filepath, 'config.json')
    with open(configfile, 'rb') as configf:
        config = json.loads(configf.read())
    return config


#testme
def make_category_string(categories):
    """Given a list of categories, return the |-separated string."""
    return '|'.join(categories)


def timelog(run_time, filepath):
    """Get the timestamp from the last run, then log the current time
    (UTC).
    """
    timelogfile = os.path.join(filepath, 'time.log') # fixme this currently only works because filepath is in the enclosing scope (main)
    try:
        with open(timelogfile, 'r+b') as timelog:
            prevruntimestamp = timelog.read()
            timelog.seek(0)
            timelog.write(datetime.datetime.strftime(run_time,
                                                     '%Y-%m-%dT%H:%M:%SZ'))
            timelog.truncate()
    except IOError:
        with open(timelogfile, 'wb') as timelog:
            prevruntimestamp = ''
            timelog.write(datetime.datetime.strftime(run_time,
                                                     '%Y-%m-%dT%H:%M:%SZ'))
    return prevruntimestamp


#testme
def buildgreeting(greeting, username, ideas):
    """Create a customized greeting string to be posted to a talk page
    to present the IdeaLab member with a list of interesting ideas.

    Return the wikitext-formatted greeting string.
    """
    idea_string = ''
    for idea in ideas:
        title = idea['profile_title']
        idea_string = u'{}* [[{}]]\n'.format(idea_string, title)
    full_greeting = greeting.format(username, idea_string)
    return full_greeting
