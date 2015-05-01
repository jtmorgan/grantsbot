import sys
import os
import json
import sqlalchemy as sqa
import datetime


def main(filepath):
    config = load_config(filepath)
    conn_str = makeconnstr(config)
    createtable(conn_str)

def load_config(filepath):
    configfile = os.path.join(filepath, 'config.json')
    with open(configfile, 'rb') as configf:
        config = json.loads(configf.read())
    return config


def makeconnstr(config):
    username = config['dbinfo']['username']
    password = config['dbinfo']['password']
    host = config['dbinfo']['host']
    dbname = config['dbinfo']['dbname']
    conn_str = 'mysql://{}:{}@{}/{}'.format(username, password, host, dbname)
    return conn_str


def createtable(conn_str):
    engine = sqa.create_engine(conn_str, echo=True)
    metadata = sqa.MetaData()
    matches = sqa.Table('matches', metadata,
                        sqa.Column('id', sqa.Integer, primary_key = True),
                        sqa.Column('participant_userid', sqa.Integer),
                        sqa.Column('p_profile_pageid', sqa.Integer),
                        sqa.Column('p_interest', sqa.String(75)),
                        sqa.Column('p_skill', sqa.String(75)),
                        sqa.Column('request_time', sqa.DateTime),
                        sqa.Column('match_time', sqa.DateTime),
                        sqa.Column('match_revid', sqa.Integer),
                        sqa.Column('idea_pageid', sqa.Integer),
                        sqa.Column('run_time', sqa.DateTime))
    metadata.create_all(engine)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = './matching/'

    main(filepath)
