#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import *

from matching.mbapi import parse_page_title_response, parse_page_info_response
from matching.mbapi import add_new_members_to_list, add_member_info


def setup():
    print('Setup!')

def teardown():
    print('Teardown!')

# tests for parse_page_title_response
def test_parse_page_title_response():
    response = {u'batchcomplete': u'', u'query': {
                    u'pages': {u'6894734': {
                    u'lastrevid': 11408043, u'pageid': 6894734,
                    u'title': u'User talk:Jmorgan (WMF)/test profile2',
                    u'length': 12343, u'contentmodel': u'wikitext',
                    u'pagelanguage': u'en',
                    u'touched': u'2015-02-27T19:25:54Z', u'ns': 3}},
                u'userinfo': {u'id': 7535326, u'name': u'MatchBot'}}}
    assert (parse_page_title_response(response) ==
            u'User talk:Jmorgan (WMF)/test profile2')

@raises(KeyError)
def test_parse_bad_page_title_response():
    parse_page_title_response({})


#tests for parse_page_info_response
def parse_good_page_info_response_setup():
    response = {u'query': {u'pages': {u'6895623':
                {u'lastrevid': 11330642, u'pageid': 6895623,
                 u'title': u'User:Jmorgan (WMF)/Jmorgan1',
                 u'length': 386, u'contentmodel': u'wikitext',
                 u'pagelanguage': u'en', u'touched': u'2015-02-20T19:33:38Z',
                 u'ns': 2, u'categories': [
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members interested in gender gap projects'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with design experience'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with programming experience'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with project management experience'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with research experience'}],
                u'revisions': [{u'userid': 1463303, u'user': u'Jmorgan (WMF)'}]
                }},
                u'userinfo': {u'id': 7535326, u'name': u'MatchBot'}},
                u'continue': {u'rvcontinue': 11330617,
                              u'continue': u'||info|categories|userinfo'},
                u'limits': {u'categories': 500}}
    user, userid, talkid, page_categories = parse_page_info_response(response)
    page_info = {'user': user, 'userid': userid, 'talkid': talkid,
                 'page categories': page_categories}
    return page_info

@raises(KeyError)
def test_parse_blank_page_info_response():
    parse_page_info_response({})

@raises(KeyError)
def test_parse_page_info_response_no_username():
    response = {u'query': {u'pages': {u'6895623':
                {u'lastrevid': 11330642, u'pageid': 6895623,
                 u'title': u'User:Jmorgan (WMF)/Jmorgan1',
                 u'length': 386, u'contentmodel': u'wikitext',
                 u'pagelanguage': u'en', u'touched': u'2015-02-20T19:33:38Z',
                 u'ns': 2, u'categories': [
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members interested in gender gap projects'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with design experience'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with programming experience'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with project management experience'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with research experience'}],
                u'revisions': [{u'userid': 1463303}]
                }},
                u'userinfo': {u'id': 7535326, u'name': u'MatchBot'}},
                u'continue': {u'rvcontinue': 11330617,
                              u'continue': u'||info|categories|userinfo'},
                u'limits': {u'categories': 500}}
    parse_page_info_response(response)

def test_parse_page_info_response_username():
    page_info = parse_good_page_info_response_setup()
    assert page_info['user'] == u'Jmorgan (WMF)'

@raises(KeyError)
def test_parse_page_info_response_no_userid():
    response = {u'query': {u'pages': {u'6895623':
                {u'lastrevid': 11330642, u'pageid': 6895623,
                 u'title': u'User:Jmorgan (WMF)/Jmorgan1',
                 u'length': 386, u'contentmodel': u'wikitext',
                 u'pagelanguage': u'en', u'touched': u'2015-02-20T19:33:38Z',
                 u'ns': 2, u'categories': [
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members interested in gender gap projects'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with design experience'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with programming experience'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with project management experience'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with research experience'}],
                u'revisions': [{u'user': u'Jmorgan (WMF)'}]
                }},
                u'userinfo': {u'id': 7535326, u'name': u'MatchBot'}},
                u'continue': {u'rvcontinue': 11330617,
                              u'continue': u'||info|categories|userinfo'},
                u'limits': {u'categories': 500}}
    parse_page_info_response(response)

def test_parse_page_info_response_userid():
    page_info = parse_good_page_info_response_setup()
    assert page_info['userid'] == 1463303

def test_parse_page_info_response_no_talkid():
    page_info = parse_good_page_info_response_setup()
    assert page_info['talkid'] is None

def test_parse_page_info_response_has_talkid():
    response = {u'query': {u'pages': {u'6895623':
                {u'lastrevid': 11330642, u'pageid': 6895623,
                 u'title': u'User:Jmorgan (WMF)/Jmorgan1',
                 u'length': 386, u'contentmodel': u'wikitext',
                 u'pagelanguage': u'en', u'touched': u'2015-02-20T19:33:38Z',
                 u'talkid': 6894840, u'ns': 2, u'categories': [
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members interested in gender gap projects'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with design experience'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with programming experience'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with project management experience'},
                    {u'ns': 14, u'title':
                u'Category:IdeaLab members with research experience'}],
                u'revisions': [{u'user': 'Chickens', u'userid': 1463303}]
                }},
                u'userinfo': {u'id': 7535326, u'name': u'MatchBot'}},
                u'continue': {u'rvcontinue': 11330617,
                              u'continue': u'||info|categories|userinfo'},
                u'limits': {u'categories': 500}}
    user, userid, talkid, page_categories = parse_page_info_response(response)
    assert talkid == 6894840

def test_parse_page_info_response_no_categories():
    response = {u'query': {u'pages': {u'6895623':
                {u'lastrevid': 11330642, u'pageid': 6895623,
                 u'title': u'User:Jmorgan (WMF)/Jmorgan1',
                 u'length': 386, u'contentmodel': u'wikitext',
                 u'pagelanguage': u'en', u'touched': u'2015-02-20T19:33:38Z',
                 u'ns': 2, u'revisions':
                    [{u'userid': 1463303, u'user': u'Jmorgan (WMF)'}]}},
                u'userinfo': {u'id': 7535326, u'name': u'MatchBot'}},
                u'continue': {u'rvcontinue': 11330617,
                              u'continue': u'||info|categories|userinfo'},
                u'limits': {u'categories': 500}}
    user, userid, talkid, page_categories = parse_page_info_response(response)
    assert page_categories is None

def test_parse_page_info_response_categories():
    page_info = parse_good_page_info_response_setup()
    page_categories = [{u'ns': 14, u'title':
        u'Category:IdeaLab members interested in gender gap projects'},
                        {u'ns': 14, u'title':
        u'Category:IdeaLab members with design experience'},
                        {u'ns': 14, u'title':
        u'Category:IdeaLab members with programming experience'},
                        {u'ns': 14, u'title':
        u'Category:IdeaLab members with project management experience'},
                        {u'ns': 14, u'title':
        u'Category:IdeaLab members with research experience'}]
    assert page_info['page categories'] == page_categories


#tests for add_new_members_to_list
def test_add_new_members_setup():
    response = {u'batchcomplete': u'',
                u'query':
                    {u'userinfo': {u'id': 7535326, u'name': u'MatchBot'},
                     u'categorymembers': [
                        {u'timestamp': u'2015-02-25T20:53:10Z',
                         u'ns': 2, u'pageid': 6950116,
                         u'title': u'User:Jmorgan (WMF)/Jmorgan (WMF)'},
                        {u'timestamp': u'2015-02-18T23:46:15Z', u'ns': 2,
                         u'pageid': 6888014,
                         u'title': u'User:Jmorgan (WMF)/test profile2'},
                        {u'timestamp': u'2015-02-18T18:28:12Z', u'ns': 2,
                         u'pageid': 6893810,
                         u'title': u'User:Jmorgan (WMF)/Test'},
                        {u'timestamp': u'2015-02-17T23:46:17Z', u'ns': 2,
                         u'pageid': 6888013,
                         u'title': u'User:Jmorgan (WMF)/test profile1'}]},
                u'limits': {u'categorymembers': 500}}
    return(response)

def test_add_no_new_members_setup():
    response = {u'batchcomplete': u'', u'limits': {u'categorymembers': 500},
                u'query': {u'categorymembers': [],
                u'userinfo': {u'id': 7535326, u'name': u'MatchBot'}}}
    return(response)

def test_add_new_members_to_nonexistent_list():
    response = test_add_new_members_setup()
    new_list = [{'cat_time': u'2015-02-25T20:53:10Z', 'category': 'Category:Chickens', 'profile_id': 6950116, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan (WMF)'}, {'cat_time': u'2015-02-18T23:46:15Z', 'category': 'Category:Chickens', 'profile_id': 6888014, 'profile_title': u'User:Jmorgan (WMF)/test profile2'}, {'cat_time': u'2015-02-18T18:28:12Z', 'category': 'Category:Chickens', 'profile_id': 6893810, 'profile_title': u'User:Jmorgan (WMF)/Test'}, {'cat_time': u'2015-02-17T23:46:17Z', 'category': 'Category:Chickens', 'profile_id': 6888013, 'profile_title': u'User:Jmorgan (WMF)/test profile1'}]
    assert add_new_members_to_list(response, 'Category:Chickens') == new_list

def test_add_new_members_to_existing_list():
    response = test_add_new_members_setup()
    existing_list = [{'category': 'Category: Not a chicken'}]

    new_list = [{'category': 'Category: Not a chicken'}, {'cat_time': u'2015-02-25T20:53:10Z', 'category': 'Category:Not chickens', 'profile_id': 6950116, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan (WMF)'}, {'cat_time': u'2015-02-18T23:46:15Z', 'category': 'Category:Not chickens', 'profile_id': 6888014, 'profile_title': u'User:Jmorgan (WMF)/test profile2'}, {'cat_time': u'2015-02-18T18:28:12Z', 'category': 'Category:Not chickens', 'profile_id': 6893810, 'profile_title': u'User:Jmorgan (WMF)/Test'}, {'cat_time': u'2015-02-17T23:46:17Z', 'category': 'Category:Not chickens', 'profile_id': 6888013, 'profile_title': u'User:Jmorgan (WMF)/test profile1'}]

    assert (add_new_members_to_list(response, 'Category:Not chickens',
                                    existing_list) == new_list)

def test_add_no_members_to_existing_list():
    response = test_add_no_new_members_setup()
    existing_list = [{'cat_time': u'2015-02-25T20:53:10Z', 'category': 'Category:Chickens', 'profile_id': 6950116, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan (WMF)'}, {'cat_time': u'2015-02-18T23:46:15Z', 'category': 'Category:Chickens', 'profile_id': 6888014, 'profile_title': u'User:Jmorgan (WMF)/test profile2'}, {'cat_time': u'2015-02-18T18:28:12Z', 'category': 'Category:Chickens', 'profile_id': 6893810, 'profile_title': u'User:Jmorgan (WMF)/Test'}, {'cat_time': u'2015-02-17T23:46:17Z', 'category': 'Category:Chickens', 'profile_id': 6888013, 'profile_title': u'User:Jmorgan (WMF)/test profile1'}]
    assert(add_new_members_to_list(response, 'Category:Chickens',
                                   existing_list) == existing_list)

def test_add_no_members_to_nonexistent_list():
    response = test_add_no_new_members_setup()
    assert add_new_members_to_list(response, 'Category:Chickens') == []

@raises(KeyError)
def test_add_blank_result_to_list():
    add_new_members_to_list({}, 'Category:Chickens')

#tests for add_member_info
def test_add_no_member_info():
    response = {u'batchcomplete': u'', u'query': {u'categorymembers': []}}
    assert add_member_info(response) == []

def test_add_member_info_to_existing_list():
    response = {u'batchcomplete': u'',
                u'limits': {u'categorymembers': 500},
                u'query': {u'categorymembers': [{u'ns': 2,
                                  u'pageid': 6895623,
                                  u'timestamp': u'2015-02-18T23:39:25Z',
                                  u'title': u'User:Jmorgan (WMF)/Jmorgan1'},
                                 {u'ns': 2,
                                  u'pageid': 6849656,
                                  u'timestamp': u'2015-02-17T23:49:45Z',
                                  u'title': u'User:Jmorgan (WMF)/sandbox/Test1'},
                                 {u'ns': 2,
                                  u'pageid': 6888013,
                                  u'timestamp': u'2015-02-17T23:46:17Z',
                                  u'title': u'User:Jmorgan (WMF)/test profile1'},
                                 {u'ns': 2,
                                  u'pageid': 6849665,
                                  u'timestamp': u'2015-02-17T23:26:32Z',
                                  u'title': u'User:Jmorgan (WMF)/sandbox/Test2'}
                                               ],
            u'userinfo': {u'id': 7535326, u'name': u'MatchBot'}}}
    member_list = [{'profileid': 6895623, 'profile_title':
                    u'User:Jmorgan (WMF)/Jmorgan1'},
                    {'profileid': 6849656, 'profile_title':
                    u'User:Jmorgan (WMF)/sandbox/Test1'},
                    {'profileid': 6888013, 'profile_title':
                    u'User:Jmorgan (WMF)/test profile1'},
                    {'profileid': 6849665, 'profile_title':
                    u'User:Jmorgan (WMF)/sandbox/Test2'}]
    new_member_list = [{'profileid': 6895623, 'profile_title':
                        u'User:Jmorgan (WMF)/Jmorgan1'},
                       {'profileid': 6849656, 'profile_title':
                        u'User:Jmorgan (WMF)/sandbox/Test1'},
                       {'profileid': 6888013, 'profile_title':
                        u'User:Jmorgan (WMF)/test profile1'},
                       {'profileid': 6849665, 'profile_title':
                        u'User:Jmorgan (WMF)/sandbox/Test2'},
                       {'profileid': 6895623, 'profile_title':
                        u'User:Jmorgan (WMF)/Jmorgan1'},
                       {'profileid': 6849656, 'profile_title':
                        u'User:Jmorgan (WMF)/sandbox/Test1'},
                       {'profileid': 6888013, 'profile_title':
                        u'User:Jmorgan (WMF)/test profile1'},
                       {'profileid': 6849665, 'profile_title':
                        u'User:Jmorgan (WMF)/sandbox/Test2'}]
    assert add_member_info(response, member_list) == new_member_list

def test_add_member_info_to_nonexistent_list():
    response = {u'batchcomplete': u'',
         u'limits': {u'categorymembers': 500},
         u'query': {u'categorymembers': [{u'ns': 2,
                                  u'pageid': 6895623,
                                  u'timestamp': u'2015-02-18T23:39:25Z',
                                  u'title': u'User:Jmorgan (WMF)/Jmorgan1'},
                                 {u'ns': 2,
                                  u'pageid': 6849656,
                                  u'timestamp': u'2015-02-17T23:49:45Z',
                                  u'title': u'User:Jmorgan (WMF)/sandbox/Test1'},
                                 {u'ns': 2,
                                  u'pageid': 6888013,
                                  u'timestamp': u'2015-02-17T23:46:17Z',
                                  u'title': u'User:Jmorgan (WMF)/test profile1'},
                                 {u'ns': 2,
                                  u'pageid': 6849665,
                                  u'timestamp': u'2015-02-17T23:26:32Z',
                                  u'title': u'User:Jmorgan (WMF)/sandbox/Test2'}],
            u'userinfo': {u'id': 7535326, u'name': u'MatchBot'}}}
    member_list = [{'profileid': 6895623, 'profile_title':
                    u'User:Jmorgan (WMF)/Jmorgan1'},
                    {'profileid': 6849656, 'profile_title':
                    u'User:Jmorgan (WMF)/sandbox/Test1'},
                    {'profileid': 6888013, 'profile_title':
                    u'User:Jmorgan (WMF)/test profile1'},
                    {'profileid': 6849665, 'profile_title':
                    u'User:Jmorgan (WMF)/sandbox/Test2'}]
    assert add_member_info(response) == member_list

@raises(KeyError)
def test_add_bad_result_to_member_info():
    response = {}
    add_member_info(response)
