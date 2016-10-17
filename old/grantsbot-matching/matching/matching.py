#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
matching
========

Like HostBot/matching, GrantsBot/matching is a MediaWiki bot that
perfoms category-based matching among pages in a given on-wiki space.
In the IdeaLab (https://meta.wikimedia.org/wiki/Grants:IdeaLab), it
leaves a message on an IdeaLab member's profile talk page (e.g.
https://meta.wikimedia.org/wiki/Grants:IdeaLab/Fhocutt_%28WMF%29) when
it detects an addition to their listed skill or interest categories. The
message lists five ideas that they may be interested in contributing to.

To run:

    $ python matching/matching.py <path-to-config-dir>

GrantsBot/matching expects to find two files in its containing
directory: time.log, a text file containing a MediaWiki-formatted
timestamp that denotes the last time the bot ran, and config.json, a
configuration file containing settings such as login information,
category names, database information, and the text of the greeting
messages to be posted. GrantsBot/matching logs information when a run
is complete, when a message is posted on a profile talk page (e.g.
https://meta.wikimedia.org/wiki/Grants_talk:IdeaLab/Fhocutt_%28WMF%29),
and when an error occurs. Error and run logs are stored in
<path-to-config-dir>/log/ .
"""

import datetime
import json
import sys
import os
import random

import mwclient

import mbapi
import mblog
import utils
import sqlutils


def main(filepath):
    run_time = datetime.datetime.utcnow()
    config = utils.load_config(filepath)
    edited_pages = False
    wrote_db = False
    logged_errors = False

    try:
        prevruntimestamp = utils.timelog(run_time, filepath)
    except Exception as e:
        mblog.logerror(u'Could not get time of previous run', exc_info=True)
        logged_errors = True
        mblog.logrun()
        sys.exit()

    try:
        site = login(config['login'])
    except mwclient.LoginError as e:
        mblog.logerror(u'Login failed for {}'.format(creds['username']),
                       exc_info=True)
        logged_errors = True
        mblog.logrun(filepath, run_time, edited_pages, wrote_db, logged_errors)
        sys.exit()

    try:
        profile_lists = get_profiles(prevruntimestamp, config['categories'],
                                     site)
        bare_profiles = filter_profiles(profile_lists[0], profile_lists[1],
                                        config['pages']['main'])
        new_profiles = get_profile_info(bare_profiles, config['categories'],
                                        config['pages'], site)
    except Exception as e:
        mblog.logerror(u'Could not construct profile dictionaries',
                       exc_info=True)
        logged_errors = True
        mblog.logrun(filepath, run_time, edited_pages, wrote_db, logged_errors)
        sys.exit()

    try:
        active_ideas = get_active_ideas(run_time, config)
    except Exception as e:
        mblog.logerror(u'Could not fetch active ideas from idealab_ideas',
                       exc_info=True)
        logged_errors = True
        mblog.logrun()
        sys.exit()

    ideas = {}

    for profile in new_profiles:
        skills = new_profiles[profile]['skills']
        interests = new_profiles[profile]['interests']

        try:
            idea_list = get_ideas_by_category(ideas, interests, skills, site,
                                              config['categories'])
            active_idea_list = filter_ideas(idea_list, active_ideas)
            final_ideas = choose_ideas(active_idea_list, 5)
        except Exception as e:
            mblog.logerror(u'Could not generate ideas for {}'.format(
                profile['profile_title']), exc_info=True)
            logged_errors = True
            continue

        # If not enough ideas, search on interest and skill individually
        if len(final_ideas) < 5:
            final_ideas = get_more_ideas(final_ideas, interests, skills, site,
                                         config['categories'])
        else:
            pass

        # If still not enough, fill from the list of all ideas
        if len(final_ideas) < 5:
            final_ideas = get_more_ideas(final_ideas, [], [], site,
                                         config['categories'])
        else:
            pass

        try:
            greeting = utils.buildgreeting(config['greetings']['greeting'],
                new_profiles[profile]['username'], final_ideas)
        except Exception as e:
            mblog.logerror(u'Could not create a greeting for {}'.format(
                learner['learner']), exc_info=True)
            logged_errors = True
            continue

        try:
            response = postinvite(new_profiles[profile]['talk_title'],
                                  greeting, 'Ideas for you', site)
            edited_pages = True
        except mwclient.MwClientError as e:
            mblog.logerror(u'Could not post match on {}\'s page'.format(
                profile['username']), exc_info=True)
            logged_errors = True
            continue

        try:
            match_info = collect_match_info(response, new_profiles[profile],
                                            final_ideas, run_time)
            sqlutils.logmatch(match_info, config['dbinfo'])
            wrote_db = True
        except Exception as e:
            mblog.logerror(u'Could not write to DB for {}'.format(
                learner['learner']), exc_info=True)
            logged_errors = True
            continue

    mblog.logrun(filepath, run_time, edited_pages, wrote_db, logged_errors)


def login(creds):
    """Initialize mwclient Site and log in."""
    site = mwclient.Site((creds['protocol'], creds['site']),
                          clients_useragent=creds['useragent'])
    site.login(creds['username'], creds['password'])
    return site


def get_profiles(prev_run_timestamp, categories, site):
    """Get the profiles needed for the script to run.

    Parameters:
        prev_run_timestamp  :   a string containing a MediaWiki-
                                formatted timestamp denoting the last
                                run of the bot
        categories          :   the 'categories' dictionary from the
                                config file
        site                :   a mwclient Site object

    Returns:
        new_profiles        :   a list of dicts with information about
                                profiles newly added to the categories
                                listed under "skills" and "topics"
                                in the config file
        opted_out_profiles  :   a list of dicts with information about
                                all opted-out members' profiles
    """
    opted_out_profiles = mbapi.get_all_category_members(
        categories['people']['optout'], site)
    all_categories = (categories['people']['skills'] +
                      categories['people']['topics'])
    new_profiles = []
    for category in all_categories:
        new_profiles = new_profiles + mbapi.get_new_members(category, site,
                                                            prev_run_timestamp)
    return (new_profiles, opted_out_profiles)


def filter_profiles(new_profiles, opted_out_profiles, prefix):
    """Filters out opted-out profiles and profiles that don't start
    with the given prefix.

    Returns a dict of dicts (one per profile), keyed by profile page
    title.
    """
    opted_out_titles = [x['profile_title'] for x in opted_out_profiles]
    profiles = {x['profile_title']: x for x in new_profiles
                if x['profile_title'].startswith(prefix)
                and x['profile_title'] not in opted_out_titles}
    return profiles


def get_profile_info(profiles, categories, prefixes, site):
    """Given a dict of profile information, fill in the rest of the
    information needed.

    Parameters:
        profiles    :   dict of profile dicts
        categories  :   categories dict from the config
        prefixes    :   prefixes dict from the config
        site        :   mwclient Site object

    Result:
        Dict of dicts, keyed by profile page title, with the following
        structure:

        {<profile page title>:
            {'username': <user name of profile creator>,
             'userid': <user id of profile creator>,
             'skills': [<first profile skill category>, ...],
             'interests': [<first profile interest category>, ...],
             'profiletitle': <profile page title>,
             'profileid': <profile page id>,
             'profiletalktitle': <profile's talk page title>},
            ...
        }
    """
    for profile in profiles:
        personcats = (categories['people']['skills']
            + categories['people']['topics'])

        page_info = mbapi.get_page_info(profile, personcats, site)
        username, userid, talk_id, page_categories = page_info

        # could probably refactor this
        profile_dict = profiles[profile]
        profile_dict['username'], profile_dict['userid'] = username, userid
        profile_dict['talk_id'] = talk_id
        profile_dict['talk_title'] = get_profile_talk_page(profile, talk_id,
                                                           prefixes, site)
        profile_dict['skills'], profile_dict['interests'] = [], []

        # we've only retrieved page categories representing skills and
        # interests, now we can sort them
        for category in page_categories:
            if category['title'] in categories['people']['skills']:
                profile_dict['skills'].append(category['title'])
            else:
                pass

            if category['title'] in categories['people']['topics']:
                profile_dict['interests'].append(category['title'])
            else:
                pass
    return profiles


def get_profile_talk_page(profile, talk_id, prefixes, site):
    """Get the talk page title for a profile (a sub-page of the IdeaLab)."""
    if talk_id:
        talkpage = mbapi.get_page_title(talk_id, site)
    else:
        talkpage = profile.replace(prefixes['main'], prefixes['talk'], 1)
    return talkpage


def get_active_ideas(run_time, config):
    """ Checks the idea database for active ideas. Also formats the
    idea titles to get them in the same form as the API returns them.
    """
    return [u'Grants:{}'.format(x[0].replace('_', ' '))
            for x in sqlutils.get_filtered_ideas(config['dbinfo'])]


def get_ideas_by_category(ideas, interests, skills, site, categories):
    """Create a dict of lists of ideas, keyed by the topic or skill
    category.

    Employs lazy loading to only fetch the ideas in the skill and
    interest categories provided.

    Parameters:
        ideas       :   a dict of ideas, empty or previously returned
                        by this method
        interests   :   a list of interest categories (topics)
        skills      :   a list of skill categories
        site        :   a mwclient Site object
        categories  :   the category dict from the config

    Returns:
        A dict of lists of ideas with the following structure:

        ideas = {topic1: [{profile: <idea profile page title>,
                           profile_id: <idea profile page id>}, ...],
                 skill1: [...],
                 skill2: [...],
                ...
                }
    """
    interest_dict = {k: v for k, v in zip(categories['people']['topics'],
                                          categories['ideas']['topics'])}
    skill_dict = {k: v for k, v in zip(categories['people']['skills'],
                                       categories['ideas']['skills'])}

    idea_interests = [interest_dict.get(interest) for interest in interests]
    idea_skills = [skill_dict.get(skill) for skill in skills]

    # Lazy loading of ideas by skill and interest
    for interest in idea_interests:
        if interest not in ideas:
            ideas[interest] = mbapi.get_all_category_members(interest, site)
        else:
            pass

    for skill in idea_skills:
        if skill not in ideas:
            ideas[skill] = mbapi.get_all_category_members(skill, site)
        else:
            pass

    if not interests and not skills and 'all' not in ideas:
        ideas['all'] = mbapi.get_all_category_members(
            categories['ideas']['all'], site)
    else:
        pass

    # Figure out which ideas are relevant to return
    ideas_list = []
    if interests and skills:
        for idea_interest in idea_interests:
            for idea_skill in idea_skills:
                filtered_ideas = [x for x in ideas[idea_skill] if x in
                                  ideas[idea_interest] and x not in ideas_list]
                ideas_list.extend(filtered_ideas)
    elif interests:
        for idea_interest in idea_interests:
            filtered_ideas = [x for x in ideas[idea_interest] if x not in
                              ideas_list]
            ideas_list.extend(filtered_ideas)
    elif skills:
        for idea_skill in idea_skills:
            filtered_ideas = [x for x in ideas[idea_skill] if x not in
                              ideas_list]
            ideas_list.extend(filtered_ideas)
    else:
        ideas_list = ideas['all']
    return ideas_list


def filter_ideas(ideas, active_ideas):
    """Create a list of ideas containing only active ideas."""
    return [x for x in ideas if x['profile_title'] in active_ideas]


def choose_ideas(ideas, number_to_choose):
    """Given a list of ideas, return a random sample of a given size.
    If there are fewer ideas than the given size (or the given size is
    negative), return the original list.
    """
    try:
        return random.sample(ideas, number_to_choose)
    except ValueError:
        return ideas


def get_more_ideas(final_ideas, interests, skills, site, config['categories']):
    """Add ideas to a given list of ideas using relaxed search criteria
    (up to 5 items in the expanded list).

    Get more ideas using the provided skills and interests categories,
    searching individually; filter for activity and add a random
    selection of the new ideas to expand the list up to 5 ideas.

    Return the expanded list.
    """
    try:
        skill_idea_list = get_ideas_by_category(ideas, [], skills, site,
                                                config['categories'])
        interest_idea_list = get_ideas_by_category(ideas, interests, [], site,
                                                   config['categories'])
        active_add_ideas = filter_ideas(skill_idea_list + interest_idea_list,
                                          active_ideas)
        unique_active_extra_ideas = [x for x in active_add_ideas if x not in 
                                     final_ideas]
        ideas_to_add = choose_ideas(unique_active_extra_ideas,
                                    5 - len(final_ideas))
        final_ideas = final_ideas + ideas_to_add
        return final_ideas

    except Exception as e:
        mblog.logrun(u'Could not get more ideas', exc_info=True)
        logged_errors = True


def postinvite(pagetitle, greeting, topic, site):
    """Add a new section to a page and return the API POST result."""
    profile = site.Pages[pagetitle]
    result = profile.save(greeting, section='new', summary=topic)
    return result


def collect_match_info(response, profile_dict, matched_ideas, run_time):
    """Prepare information about matches made to be added to the
    matches database table. Return a list of dicts, where each
    dict is a row to add to the database.
    """
    match_info = []
    for idea in matched_ideas:
        match_info.append({
            'participant_userid': profile_dict['userid'],
            'p_profile_pageid': profile_dict['profile_id'],
            'p_interest': None,
            'p_skill': None,
            'request_time': utils.parse_timestamp(profile_dict['cat_time']),
            'match_time': utils.parse_timestamp(response['newtimestamp']),
            'match_revid': response['newrevid'],
            'idea_pageid': idea['profileid'],
            'run_time': run_time
        })
    return match_info


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = './matching/'

    main(filepath)
