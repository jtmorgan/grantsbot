#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import *
import datetime

from matching.utils import parse_timestamp, make_category_string, buildgreeting

def setup():
    print('Setup!')

def teardown():
    print('Teardown!')

def test_basic():
    print('I RAN!')

#tests for parse_timestamp
@raises(ValueError)
def test_parse_blank_timestamp():
    parse_timestamp('')


def test_parse_zero_timestamp():
    assert parse_timestamp('0000-00-00T00:00:00Z') == None


def test_parse_expected_timestamp():
    assert (parse_timestamp('2010-10-10T01:01:10Z') ==
            datetime.datetime(2010, 10, 10, 01, 01, 10))


@raises(ValueError)
def test_parse_timestamp_random_string():
    parse_timestamp('spam')


#tests for make_category_string
def test_make_category_string_three_items_unicode():
    category_list = [u'Category:Chickens', u'Category:Fowl', u'Category:Chickens \u2013 Unicode']
    print(make_category_string(category_list))
    assert make_category_string(category_list) == u'Category:Chickens|Category:Fowl|Category:Chickens \u2013 Unicode'


def test_make_category_string_one_item():
    category_list = [u'Category:Chickens']
    assert make_category_string(category_list) == u'Category:Chickens'


def test_make_category_string_empty_list():
    assert make_category_string([]) == ''


# tests for buildgreeting
def test_buildgreeting_one_idea_ascii():
    greeting = u'Welcome to the IdeaLab, [[User:{0}|{0}]]! ' \
               u'Here are some ideas that you may want to check out:\n{1}Take' \
               u' a look and endorse them, help improve them, or spread the ' \
               u'word. --~~~~'
    ideas = [{'profileid': 5793487,
              'profile_title': u'Grants:IdeaLab/Gender-gap admin training'}]
    assert (buildgreeting(greeting, 'ChickensAreCool', ideas) ==
            "Welcome to the IdeaLab, [[User:ChickensAreCool|ChickensAreCool]]! Here are some ideas that you may want to check out:\n* [[Grants:IdeaLab/Gender-gap admin training]]\nTake a look and endorse them, help improve them, or spread the word. --~~~~"
    )


def test_buildgreeting_two_ideas_unicode():
    greeting = u'Welcome to the IdeaLab, [[User:{0}|{0}]]! ' \
               u'Here are some ideas that you may want to check out:\n{1}Take' \
               u' a look and endorse them, help improve them, or spread the ' \
               u'word. --~~~~'
    ideas = [{'profileid': 5793487,
              'profile_title': u'Grants:IdeaLab/Gender-gap admin training'},
             {'profileid': 5322427,
              'profile_title': u'Grants:IdeaLab/Inspire Grants \u2013 Gender gap campaign'}]
    print(buildgreeting(greeting, 'ChickensAreCool', ideas))
    assert (buildgreeting(greeting, 'ChickensAreCool', ideas) ==
    u'Welcome to the IdeaLab, [[User:ChickensAreCool|ChickensAreCool]]! Here are some ideas that you may want to check out:\n* [[Grants:IdeaLab/Gender-gap admin training]]\n* [[Grants:IdeaLab/Inspire Grants \u2013 Gender gap campaign]]\nTake a look and endorse them, help improve them, or spread the word. --~~~~'
    )
