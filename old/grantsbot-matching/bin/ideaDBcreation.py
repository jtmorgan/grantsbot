import sys
import os
import json
import sqlalchemy as sqa
import datetime

from matching.sqlutils import make_conn_string
from matching.utils import load_config

def main(filepath):
    config = load_config(filepath)  # filepath should be the path to the config
    conn_str = make_conn_string(config)
    createtable(conn_str)


def createtable(conn_str):
    '''Create a table with the following schema:
+---------------------+------------------+------+-----+---------+----------------+
| Field               | Type             | Null | Key | Default | Extra          |
+---------------------+------------------+------+-----+---------+----------------+
| id                  | int(11) unsigned | NO   | PRI | NULL    | auto_increment |
| idea_id             | int(11)          | YES  | UNI | NULL    |                |
| idea_title          | varbinary(255)   | YES  |     | NULL    |                |
| idea_talk_id        | int(11)          | YES  |     | NULL    |                |
| idea_creator        | varbinary(255)   | YES  |     | NULL    |                |
| idea_created        | datetime         | YES  |     | NULL    |                |
| idea_endorsements   | int(11)          | YES  |     | NULL    |                |
| idea_recent_editors | int(11)          | YES  |     | NULL    |                |
| ignore              | tinyint(1)       | YES  |     | 0       |                |
+---------------------+------------------+------+-----+---------+----------------+
    '''
    engine = sqa.create_engine(conn_str, echo=True)
    metadata = sqa.MetaData()
    matches = sqa.Table('idealab_ideas', metadata,
                        sqa.Column('id', sqa.Integer, primary_key = True),
                        sqa.Column('idea_id', sqa.Integer, unique=True),
                        sqa.Column('idea_title', sqa.String(255)),
                        sqa.Column('idea_talk_id', sqa.Integer),
                        sqa.Column('idea_creator', sqa.String(255)),
                        sqa.Column('idea_created', sqa.DateTime),
                        sqa.Column('idea_endorsements', sqa.Integer),
                        sqa.Column('idea_recent_editors', sqa.Integer),
                        sqa.Column('"ignore"', sqa.Boolean, default=0))
    metadata.create_all(engine)


def mangle_datetime(ideas_list):
    '''Convert a string-formatted datetime back into a datetime object.'''
    idea_list_copy = ideas_list[:]
    for idea in ideas_list:
        time_created = idea['idea_created']
        idea['idea_created'] = datetime.datetime.strptime(time_created, '%Y-%m-%d %H:%M:%S')


def load_ideas(filepath):
    '''Read a list of data out of a json file.'''
    with open('newideas.json', 'rb') as ideas:
        ideas_list = json.loads(ideas.read())
    return ideas_list


def insert_matches(conn_str, ideas_list):
    '''Insert the list of data-containing tuples (one per row) into the
    database denoted by the connection string.'''
    engine = sqa.create_engine(conn_str, echo=True)
    metadata = sqa.MetaData()
    ideas = sqa.Table('idealab_ideas', metadata, autoload=True,
                        autoload_with=engine)
    ins = ideas.insert()
    conn = engine.connect()
    conn.execute(ins, ideas_list)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = './matching/'

    main(filepath)
