#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from nose.tools import *

from matching.matching import filter_profiles, get_profile_talk_page, filter_ideas, choose_ideas, collect_match_info


def setup():
    print('Setup!')


def teardown():
    print('Teardown!')

# test cases for filter_profiles
def test_filter_profiles():
    new_profiles = [{'cat_time': u'2015-02-19T03:03:53Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6887990, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test3'}, {'cat_time': u'2015-02-19T03:03:42Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6888014, 'profile_title': u'User:Jmorgan (WMF)/test profile2'}, {'cat_time': u'2015-02-18T23:39:25Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6895623, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan1'}, {'cat_time': u'2015-02-18T20:35:22Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6888016, 'profile_title': u'User:Jmorgan (WMF)/test profile3'}, {'cat_time': u'2015-02-25T20:53:10Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6950116, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan (WMF)'}, {'cat_time': u'2015-02-19T02:39:21Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6887990, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test3'}, {'cat_time': u'2015-02-18T23:39:25Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6895623, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan1'}, {'cat_time': u'2015-02-17T23:48:26Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6888016, 'profile_title': u'User:Jmorgan (WMF)/test profile3'}, {'cat_time': u'2015-02-17T23:46:57Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6888014, 'profile_title': u'User:Jmorgan (WMF)/test profile2'}, {'cat_time': u'2015-02-18T18:28:12Z', 'category': u'Category:IdeaLab members interested in global south projects', 'profile_id': 6893810, 'profile_title': u'User:Jmorgan (WMF)/Test'}, {'cat_time': u'2015-02-17T23:46:17Z', 'category': u'Category:IdeaLab members interested in global south projects', 'profile_id': 6888013, 'profile_title': u'User:Jmorgan (WMF)/test profile1'}]
    opted_out_profiles = [{'profileid': 6849665, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test2'}, {'profileid': 6849665, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test3'}]
    prefix = u'User:Jmorgan (WMF)/'
    result = {u'User:Jmorgan (WMF)/Jmorgan1': {'cat_time': u'2015-02-18T23:39:25Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6895623, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan1'}, u'User:Jmorgan (WMF)/Test': {'cat_time': u'2015-02-18T18:28:12Z', 'category': u'Category:IdeaLab members interested in global south projects', 'profile_id': 6893810, 'profile_title': u'User:Jmorgan (WMF)/Test'}, u'User:Jmorgan (WMF)/Jmorgan (WMF)': {'cat_time': u'2015-02-25T20:53:10Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6950116, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan (WMF)'}, u'User:Jmorgan (WMF)/test profile2': {'cat_time': u'2015-02-17T23:46:57Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6888014, 'profile_title': u'User:Jmorgan (WMF)/test profile2'}, u'User:Jmorgan (WMF)/test profile3': {'cat_time': u'2015-02-17T23:48:26Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6888016, 'profile_title': u'User:Jmorgan (WMF)/test profile3'}, u'User:Jmorgan (WMF)/test profile1': {'cat_time': u'2015-02-17T23:46:17Z', 'category': u'Category:IdeaLab members interested in global south projects', 'profile_id': 6888013, 'profile_title': u'User:Jmorgan (WMF)/test profile1'}}
    filtered_profiles = filter_profiles(new_profiles, opted_out_profiles, prefix)
    assert filtered_profiles == result

def test_filter_no_profiles():
    opted_out_profiles = [{'profileid': 6849665, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test2'}, {'profileid': 6849665, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test3'}]
    filtered_profiles = filter_profiles([], opted_out_profiles, u'User:Jmorgan (WMF)/')
    assert filtered_profiles == {}

def test_filter_profiles_empty_prefix():
    new_profiles = [{'cat_time': u'2015-02-19T03:03:53Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6887990, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test3'}, {'cat_time': u'2015-02-19T03:03:42Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6888014, 'profile_title': u'User:Jmorgan (WMF)/test profile2'}, {'cat_time': u'2015-02-18T23:39:25Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6895623, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan1'}, {'cat_time': u'2015-02-18T20:35:22Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6888016, 'profile_title': u'User:Jmorgan (WMF)/test profile3'}, {'cat_time': u'2015-02-25T20:53:10Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6950116, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan (WMF)'}, {'cat_time': u'2015-02-19T02:39:21Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6887990, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test3'}, {'cat_time': u'2015-02-18T23:39:25Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6895623, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan1'}, {'cat_time': u'2015-02-17T23:48:26Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6888016, 'profile_title': u'User:Jmorgan (WMF)/test profile3'}, {'cat_time': u'2015-02-17T23:46:57Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6888014, 'profile_title': u'User:Jmorgan (WMF)/test profile2'}, {'cat_time': u'2015-02-18T18:28:12Z', 'category': u'Category:IdeaLab members interested in global south projects', 'profile_id': 6893810, 'profile_title': u'User:Jmorgan (WMF)/Test'}, {'cat_time': u'2015-02-17T23:46:17Z', 'category': u'Category:IdeaLab members interested in global south projects', 'profile_id': 6888013, 'profile_title': u'User:Jmorgan (WMF)/test profile1'}]

    opted_out_profiles = [{'profileid': 6849665, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test2'}, {'profileid': 6849665, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test3'}]
    filtered_profiles = filter_profiles(new_profiles, opted_out_profiles, u'')
    desired_result = {u'User:Jmorgan (WMF)/Jmorgan1': {'cat_time': u'2015-02-18T23:39:25Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6895623, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan1'}, u'User:Jmorgan (WMF)/Test': {'cat_time': u'2015-02-18T18:28:12Z', 'category': u'Category:IdeaLab members interested in global south projects', 'profile_id': 6893810, 'profile_title': u'User:Jmorgan (WMF)/Test'}, u'User:Jmorgan (WMF)/Jmorgan (WMF)': {'cat_time': u'2015-02-25T20:53:10Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6950116, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan (WMF)'}, u'User:Jmorgan (WMF)/test profile2': {'cat_time': u'2015-02-17T23:46:57Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6888014, 'profile_title': u'User:Jmorgan (WMF)/test profile2'}, u'User:Jmorgan (WMF)/test profile3': {'cat_time': u'2015-02-17T23:48:26Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6888016, 'profile_title': u'User:Jmorgan (WMF)/test profile3'}, u'User:Jmorgan (WMF)/test profile1': {'cat_time': u'2015-02-17T23:46:17Z', 'category': u'Category:IdeaLab members interested in global south projects', 'profile_id': 6888013, 'profile_title': u'User:Jmorgan (WMF)/test profile1'}}
    assert filtered_profiles == desired_result

def test_filter_profiles_empty_filter_no_prefix():
    new_profiles = [{'cat_time': u'2015-02-19T03:03:53Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6887990, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test3'}, {'cat_time': u'2015-02-19T03:03:42Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6888014, 'profile_title': u'User:Jmorgan (WMF)/test profile2'}, {'cat_time': u'2015-02-18T23:39:25Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6895623, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan1'}, {'cat_time': u'2015-02-18T20:35:22Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6888016, 'profile_title': u'User:Jmorgan (WMF)/test profile3'}, {'cat_time': u'2015-02-25T20:53:10Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6950116, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan (WMF)'}, {'cat_time': u'2015-02-19T02:39:21Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6887990, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test3'}, {'cat_time': u'2015-02-18T23:39:25Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6895623, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan1'}, {'cat_time': u'2015-02-17T23:48:26Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6888016, 'profile_title': u'User:Jmorgan (WMF)/test profile3'}, {'cat_time': u'2015-02-17T23:46:57Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6888014, 'profile_title': u'User:Jmorgan (WMF)/test profile2'}, {'cat_time': u'2015-02-18T18:28:12Z', 'category': u'Category:IdeaLab members interested in global south projects', 'profile_id': 6893810, 'profile_title': u'User:Jmorgan (WMF)/Test'}, {'cat_time': u'2015-02-17T23:46:17Z', 'category': u'Category:IdeaLab members interested in global south projects', 'profile_id': 6888013, 'profile_title': u'User:Jmorgan (WMF)/test profile1'}]
    opted_out_profiles = []
    prefix = u''
    filtered_profiles = filter_profiles(new_profiles, opted_out_profiles, prefix)
    desired_result = {u'User:Jmorgan (WMF)/Jmorgan1': {'cat_time': u'2015-02-18T23:39:25Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6895623, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan1'}, u'User:Jmorgan (WMF)/sandbox/Test3': {'cat_time': u'2015-02-19T02:39:21Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6887990, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test3'}, u'User:Jmorgan (WMF)/Test': {'cat_time': u'2015-02-18T18:28:12Z', 'category': u'Category:IdeaLab members interested in global south projects', 'profile_id': 6893810, 'profile_title': u'User:Jmorgan (WMF)/Test'}, u'User:Jmorgan (WMF)/Jmorgan (WMF)': {'cat_time': u'2015-02-25T20:53:10Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6950116, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan (WMF)'}, u'User:Jmorgan (WMF)/test profile2': {'cat_time': u'2015-02-17T23:46:57Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6888014, 'profile_title': u'User:Jmorgan (WMF)/test profile2'}, u'User:Jmorgan (WMF)/test profile3': {'cat_time': u'2015-02-17T23:48:26Z', 'category': u'Category:IdeaLab members interested in gender gap projects', 'profile_id': 6888016, 'profile_title': u'User:Jmorgan (WMF)/test profile3'}, u'User:Jmorgan (WMF)/test profile1': {'cat_time': u'2015-02-17T23:46:17Z', 'category': u'Category:IdeaLab members interested in global south projects', 'profile_id': 6888013, 'profile_title': u'User:Jmorgan (WMF)/test profile1'}}
    assert filtered_profiles == desired_result

@raises(KeyError)
def test_filter_bad_profiles():
    bad_profiles = [{'cat_time': u'2015-02-19T03:03:53Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6887990}, {'cat_time': u'2015-02-19T03:03:42Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6888014}, {'cat_time': u'2015-02-18T23:39:25Z', 'category': u'Category:IdeaLab members with project management experience', 'profile_id': 6895623, 'profile_title': u'User:Jmorgan (WMF)/Jmorgan1'}]
    opted_out_profiles = [{'profileid': 6849665, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test2'}, {'profileid': 6849665, 'profile_title': u'User:Jmorgan (WMF)/sandbox/Test3'}]
    filter_profiles(bad_profiles, opted_out_profiles, u'')

@raises(KeyError)
def test_filter_profiles_bad_filter():
    opted_out_profiles = [{'profileid': 6849665}, {'profileid': 6849665}]
    filter_profiles([], opted_out_profiles, '')


# test cases for get_profile_talk_page
def test_get_profile_talk_page_no_talkpage_substring_in_prefix():
    profile = u'User:Jmorgan (WMF)/Jmorgan1'
    profile_talk = u'User talk:Jmorgan (WMF)/Jmorgan1'
    prefixes = {'main': 'User:Jmorgan (WMF)/', 'talk': 'User talk:Jmorgan (WMF)/'}
    print get_profile_talk_page(profile, None, prefixes, None)
    assert get_profile_talk_page(profile, None, prefixes, None) == profile_talk

def test_get_profile_talk_page_no_talkpage():
    profile = u'User:Jmorgan (WMF)/ChickensAreCool'
    profile_talk = u'User talk:Jmorgan (WMF)/ChickensAreCool'
    prefixes = {'main': 'User:Jmorgan (WMF)/', 'talk': 'User talk:Jmorgan (WMF)/'}
    assert get_profile_talk_page(profile, None, prefixes, None) == profile_talk

def test_get_profile_talk_page_no_talkpage_nonascii():
    profile = u'User:Jmorgan (WMF)/ĞğÜüÖöçÇ'
    profile_talk = u'User talk:Jmorgan (WMF)/ĞğÜüÖöçÇ'
    prefixes = {'main': 'User:Jmorgan (WMF)/', 'talk': 'User talk:Jmorgan (WMF)/'}
    print get_profile_talk_page(profile, None, prefixes, None)
    assert get_profile_talk_page(profile, None, prefixes, None) == profile_talk


# test cases for filter_ideas
def test_filter_no_ideas():
    ideas = []
    result = filter_ideas(ideas, ['Ideas for the manticore gap'])
    assert result == ideas

def test_filter_no_ideas_no_filter():
    assert filter_ideas([], []) == []

@raises(TypeError)
def test_filter_ideas_ideas_list_of_strings():
    ideas = ['ideas', 'more ideas']
    filter_ideas(ideas, [])

def test_filter_ideas_no_filter():
    ideas = [{'profileid': 5590171, 'profile_title': u'Grants:IdeaLab/Annual training for Administrators, ArbCom, Wikimedia, and Chapter leaders'}, {'profileid': 6487284, 'profile_title': u'Grants:IdeaLab/Code of conduct synchronization'}, {'profileid': 5939165, 'profile_title': u'Grants:IdeaLab/Gender Gap Allies training'}, {'profileid': 5589969, 'profile_title': u'Grants:IdeaLab/Gender gap on the mainpage'}, {'profileid': 5793487, 'profile_title': u'Grants:IdeaLab/Gender-gap admin training'}, {'profileid': 5322427, 'profile_title': u'Grants:IdeaLab/Inspire Grants \u2013 Gender gap campaign'}, {'profileid': 6888558, 'profile_title': u'Grants:IdeaLab/Wikipedia Gender Concerns Reporting Tools'}, {'profileid': 6594508, 'profile_title': u'Grants:IdeaLab/WikiProject Men'}, {'profileid': 6686665, 'profile_title': u'Grants:IdeaLab/WIGI: Wikipedia Gender Index Tools'}]
    assert filter_ideas(ideas, []) == []

@raises(KeyError)
def test_filter_ideas_dicts_missing_profile_title():
    ideas = [{'profileid': 5590171}, {'profileid': 6487284}]
    filter_ideas(ideas, [])

def test_filter_ideas_applicable_filter():
    ideas = [{'profileid': 5590171, 'profile_title': u'Grants:IdeaLab/Annual training for Administrators, ArbCom, Wikimedia, and Chapter leaders'}, {'profileid': 6487284, 'profile_title': u'Grants:IdeaLab/Code of conduct synchronization'}, {'profileid': 5939165, 'profile_title': u'Grants:IdeaLab/Gender Gap Allies training'}, {'profileid': 5589969, 'profile_title': u'Grants:IdeaLab/Gender gap on the mainpage'}, {'profileid': 5793487, 'profile_title': u'Grants:IdeaLab/Gender-gap admin training'}, {'profileid': 5322427, 'profile_title': u'Grants:IdeaLab/Inspire Grants \u2013 Gender gap campaign'}, {'profileid': 6888558, 'profile_title': u'Grants:IdeaLab/Wikipedia Gender Concerns Reporting Tools'}, {'profileid': 6594508, 'profile_title': u'Grants:IdeaLab/WikiProject Men'}, {'profileid': 6686665, 'profile_title': u'Grants:IdeaLab/WIGI: Wikipedia Gender Index Tools'}]

    active_ideas = [u'Grants:IdeaLab/Translation platform: Minority Translate', u'Grants:IdeaLab/Human resources complaint processing best practices', u'Grants:IdeaLab/Code of conduct synchronization', u'Grants:IdeaLab/Investigation about wikimedia projects in Tunisia', u'Grants:IdeaLab/WikiProject Women', u'Grants:IdeaLab/Add Indian Classical Music to Wikipedia', u'Grants:IdeaLab/Human resources sharing in the open movement']
    desired_result = [{'profileid': 6487284, 'profile_title': u'Grants:IdeaLab/Code of conduct synchronization'}]
    assert filter_ideas(ideas, active_ideas) == desired_result

def test_filter_ideas_filter_not_applicable():
    ideas = [{'profileid': 5590171, 'profile_title': u'Grants:IdeaLab/Annual training for Administrators, ArbCom, Wikimedia, and Chapter leaders'}, {'profileid': 6487284, 'profile_title': u'Grants:IdeaLab/Code of conduct synchronization'}]
    filtered_ideas = filter_ideas(ideas, ['Ideas for the manticore gap'])
    assert filtered_ideas == []


# test cases for choose_ideas
def test_choose_ideas_no_ideas():
    assert choose_ideas([], 3) == []

def test_choose_ideas_fewer_ideas_than_number():
    assert choose_ideas(['a'], 2) == ['a']

def test_choose_ideas_negative_number():
    assert choose_ideas(['a'], -1) == ['a']

def test_choose_ideas_same_ideas_as_number():
    result = choose_ideas(['a', 'b'], 2)
    assert result in [['a', 'b'], ['b', 'a']]

def test_choose_ideas_more_ideas_than_number():
    result = choose_ideas(['a', 'b', 'c'], 2)
    possible_results = [['a', 'b'], ['a', 'c'], ['b', 'c'],
                        ['b', 'a'], ['c', 'a'], ['c', 'b']]
    assert result in possible_results

def test_choose_zero_ideas():
    assert choose_ideas(['a'], 0) == []


# tests for collect_match_info
# Possible additional tests: various keyerrors, no profile_dict, empty matched ideas, valid run_time, good/empty response
def test_collect_match_info():
    response = {u'pageid': 6895625, u'title': u'User talk:Jmorgan (WMF)/1', u'newtimestamp': u'2015-02-28T02:26:44Z', u'contentmodel': u'wikitext', u'result': u'Success', u'oldrevid': 11408050, u'newrevid': 11410968}
    matched_ideas = [{'profileid': 6487284, 'profile_title': u'Grants:IdeaLab/Code of conduct synchronization'}, {'profileid': 6431317, 'profile_title': u'Grants:IdeaLab/Translation platform: Minority Translate'}, {'profileid': 6571034, 'profile_title': u'Grants:IdeaLab/Add Indian Classical Music to Wikipedia'}, {'profileid': 6543312, 'profile_title': u'Grants:IdeaLab/Investigation about wikimedia projects in Tunisia'}, {'profileid': 6569632, 'profile_title': u'Grants:IdeaLab/WikiProject Women'}]

    profile_dict = {'category': u'Category:IdeaLab members interested in gender gap projects', 'username': u'Jmorgan (WMF)', 'talk_title': u'User talk:Jmorgan (WMF)/1', 'interests': [u'Category:IdeaLab members interested in gender gap projects'], 'skills': [u'Category:IdeaLab members with design experience', u'Category:IdeaLab members with programming experience', u'Category:IdeaLab members with project management experience', u'Category:IdeaLab members with research experience'], 'profile_id': 6895623, 'userid': 1463303, 'talk_id': None, 'cat_time': u'2015-02-18T23:39:25Z', 'profile_title': u'User:Jmorgan (WMF)/Jmorgan1'}

    run_time = datetime.datetime(2015, 2, 28, 2, 26, 38, 199228)
    desired_result = [{'run_time': datetime.datetime(2015, 2, 28, 2, 26, 38, 199228), 'match_revid': 11410968, 'match_time': datetime.datetime(2015, 2, 28, 2, 26, 44), 'p_interest': None, 'request_time': datetime.datetime(2015, 2, 18, 23, 39, 25), 'participant_userid': 1463303, 'idea_pageid': 6487284, 'p_skill': None, 'p_profile_pageid': 6895623}, {'run_time': datetime.datetime(2015, 2, 28, 2, 26, 38, 199228), 'match_revid': 11410968, 'match_time': datetime.datetime(2015, 2, 28, 2, 26, 44), 'p_interest': None, 'request_time': datetime.datetime(2015, 2, 18, 23, 39, 25), 'participant_userid': 1463303, 'idea_pageid': 6431317, 'p_skill': None, 'p_profile_pageid': 6895623}, {'run_time': datetime.datetime(2015, 2, 28, 2, 26, 38, 199228), 'match_revid': 11410968, 'match_time': datetime.datetime(2015, 2, 28, 2, 26, 44), 'p_interest': None, 'request_time': datetime.datetime(2015, 2, 18, 23, 39, 25), 'participant_userid': 1463303, 'idea_pageid': 6571034, 'p_skill': None, 'p_profile_pageid': 6895623}, {'run_time': datetime.datetime(2015, 2, 28, 2, 26, 38, 199228), 'match_revid': 11410968, 'match_time': datetime.datetime(2015, 2, 28, 2, 26, 44), 'p_interest': None, 'request_time': datetime.datetime(2015, 2, 18, 23, 39, 25), 'participant_userid': 1463303, 'idea_pageid': 6543312, 'p_skill': None, 'p_profile_pageid': 6895623}, {'run_time': datetime.datetime(2015, 2, 28, 2, 26, 38, 199228), 'match_revid': 11410968, 'match_time': datetime.datetime(2015, 2, 28, 2, 26, 44), 'p_interest': None, 'request_time': datetime.datetime(2015, 2, 18, 23, 39, 25), 'participant_userid': 1463303, 'idea_pageid': 6569632, 'p_skill': None, 'p_profile_pageid': 6895623}]
    assert collect_match_info(response, profile_dict, matched_ideas, run_time) == desired_result
