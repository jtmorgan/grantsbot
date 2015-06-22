#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
sqlutils
========

Database utility functions for matching.py.

"""

import datetime

import sqlalchemy as sqa
from sqlalchemy.sql import select, and_

def get_filtered_ideas(db_info):
    """Fetch titles of active IdeaLab ideas.

    Selects ideas that have more than 1 recent editors, have been
    updated in the last 90 days, and which are not flagged as "ignore".

    Expected MySQL database columns in the "idealab_ideas" table:
        idea_id INTEGER(11),
        idea_title VARCHAR(255),
        idea_talk_id INTEGER(11),
        idea_creator VARCHAR(255),
        idea_created DATETIME,
        idea_endorsements INTEGER(11),
        idea_recent_editors INTEGER(11),
        ignore BOOLEAN,

    Parameters:
        db_info :   dict from the config containing DB connection
                    information

    Returns:
        data    :   a list of active and non-flagged idea page titles
    """
    conn_str = make_conn_string(db_info)
#    conn_str = 'sqlite:////home/fhocutt/WMFContractWork/IdeaLab/grantsbot-matching/ideas.db'
    engine = sqa.create_engine(conn_str, echo=False)
    metadata = sqa.MetaData()
    ideas = sqa.Table('idealab_ideas', metadata, autoload=True,
                        autoload_with=engine)
#    s = select([ideas.c.idea_title]).where(and_(ideas.c.idea_recent_editors > 1,
#        ideas.c.idea_created > (datetime.datetime.utcnow() - datetime.timedelta(days=90))))
    s = select([ideas.c.idea_title]).where(and_(and_(
        ideas.c.idea_recent_editors > 1,
            ideas.c.idea_created > (datetime.datetime.utcnow() -
                datetime.timedelta(days=90))), ideas.c.ignore == 0))
    conn = engine.connect()
    result = conn.execute(s)
    data = result.fetchall()
    return data


def logmatch(match_info, db_info):
    """Log information about a match to the corresponding database.

    Expected MySQL database columns in the "matches" table:
        participant_userid INTEGER(11),
        p_profile_pageid INTEGER(11),
        p_interest VARCHAR(75),
        p_skill VARCHAR(75),
        request_time DATETIME,
        match_time DATETIME,
        match_revid INTEGER(11),
        idea_pageid INTEGER(11),
        run_time DATETIME

    Parameters:
    match_info  :   list of dicts with the following structure:
                       {'participant_userid': <userid>,
                        'p_profile_pageid': <user's profile pageid>,
                        'p_interest': None,
                        'p_skill': None,
                        'request_time': <datetime request was made>,
                        'match_time': <datetime match was delivered>,
                        'match_revid': <revid of posted message>,
                        'idea_pageid': <pageid of matched page>,
                        'run_time': <datetime script started run>}
    db_info     :   dict from the configuration

    Returns: None
    """
    conn_str = make_conn_string(db_info)
#    conn_str = 'sqlite:////home/fhocutt/WMFContractWork/IdeaLab/grantsbot-matching/matches.db'
    engine = sqa.create_engine(conn_str, echo=True)
    metadata = sqa.MetaData()
    matches = sqa.Table('matches', metadata, autoload=True,
                        autoload_with=engine)
    ins = matches.insert()
    conn = engine.connect()
    conn.execute(ins, match_info)


def make_conn_string(dbinfo):
    """Return a string with MySQL DB connecting information."""
    username = dbinfo['user']
    password = dbinfo['password']
    host = dbinfo['host']
    dbname = dbinfo['dbname']
    conn_str = 'mysql://{}:{}@{}/{}?charset=utf8&use_unicode=0'.format(
        username, password, host, dbname)
    return conn_str
