#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import *

from matching.sqlutils import make_conn_string

def test_make_conn_string():
    db_info = {'user': 'coolchickens', 'password': 'ILoveChickens',
              'host': 'chickenwiki', 'dbname': 'chicken_info'}
    assert make_conn_string(db_info) == 'mysql://coolchickens:ILoveChickens@chickenwiki/chicken_info?charset=utf8&use_unicode=0'

@raises(KeyError)
def test_make_conn_string_bad_db_info():
    db_info = {'user': 'coolchickens', 'password': 'ILoveChickens',
              'host': 'chickenwiki'}
    make_conn_string(db_info)
