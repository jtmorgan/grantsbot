#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

import mwclient

import cnf

def main():
    creds = {'protocol': cnf.protocol,
             'site': cnf.site,
             'useragent': cnf.useragent,
             'username': cnf.username,
             'password': cnf.password}
    site = login(creds)

    # get data for scoreboard
    new_participants = get_new_participant_count(site)
    inspire_idea_count = get_inspire_idea_count(site)
    days_left = calculate_days_left()

    # fill in template with data
    text_to_post = format_template(inspire_idea_count, new_participants,
                                   days_left)
    # post updated template
    update_templates(text_to_post, site)


def login(creds):
    """Initialize mwclient Site and log in."""
    site = mwclient.Site((creds['protocol'], creds['site']),
                          clients_useragent=creds['useragent'])
    site.login(creds['username'], creds['password'])
    return site


def get_new_participant_count(site):
    """Get the count of all logged-in contributors to pages in the main
    Inspire namespace and to their associated talk pages, if any.
    """
    page_ids = get_page_ids(site)
    page_ids.extend(get_talk_page_ids(page_ids, site))
    participants = get_participants(page_ids, site)
    return len(set(participants))


def get_page_ids(site):
    """Get a list of strings containing the pageids of all members of
    Category:IdeaLab/Ideas/Inspire and Category:Inspire campaign."""
    categories = ['Category:IdeaLab', 'Category:IdeaLab/Ideas/Inspire/Knowledge_networks', 'Category:Inspire_campaign']
    pageids = []
    for category in categories:
        kwargs = {'action': 'query',
                  'list': 'categorymembers',
                  'cmtitle': category,
                  'cmlimit': 'max'}
        response = site.api(**kwargs)
        for result in response['query']['categorymembers']:
            pageids.append(str(result['pageid']))
    return pageids


def get_participants(page_ids, site):
    """Given a list of pageids, get the people who have edited them
    since 31May2016."""
    contributors = []
    for page_id in page_ids:
        response = site.api(action='query', prop='revisions', rvstart='2016-01-31T00:00:00Z', rvlimit='max', pageids=page_id, rvprop='userid', rvdir='newer')
        revisions = response['query']['pages'][page_id].get('revisions')
        if revisions:
            for revision in revisions:
                contributors.append(revision['userid'])
    return contributors


def get_talk_page_ids(page_ids, site):
    """Given a list of page ids, get a list of page ids of the
    corresponding talk pages (if they exist)."""
    page_ids_string = '|'.join(page_ids)
    response = site.api(action='query',
                            prop='info',
                            inprop='talkid',
                            pageids=page_ids_string)
    pages = response['query']['pages']
    talk_page_ids = []
    for page in pages:
        if pages[page]['ns'] == 200 and pages[page].get('talkid'):
            talk_page_ids.append(str(pages[page]['talkid']))
    return talk_page_ids


def get_inspire_idea_count(site):
    """Get the number of pages in Category:IdeaLab/Ideas/Inspire, and
    correct for the three that are templates, not ideas."""
    response = site.api(action='query',
                        prop='categoryinfo',
                        titles='Category:IdeaLab/Ideas/Inspire/Addressing_harassment')
    page_count = parse_idea_count_response(response)

    # don't count probox, etc
   # actual_page_count = page_count - 3
    return page_count


def parse_idea_count_response(response):
    for page in response['query']['pages']:
        page_count = response['query']['pages'][page]['categoryinfo']['pages']
        return page_count


def calculate_days_left():
    """Calculate the number of days until June 30, 2016. If the date
    has passed, return 0."""
    ending_date = datetime.date(2016, 07, 01)
    days_left = (ending_date - datetime.date.today()).days
    if days_left >= 0:
        return days_left
    else:
        return 0


def format_template(ideas, participants, days_left):
    """Put the collected data in the template."""
    filled_template = '{{{{IdeaLab/Inspire/Scoreboard\n|ideas= {}\n|'\
                      'participants= {}\n|'\
                      'days_left= {}\n}}}}'.format(ideas, participants,
                                                   days_left)
    return filled_template


def update_templates(text_to_post, site):
    """"""
    scoreboard = site.Pages['Grants:IdeaLab/Inspire/Scoreboard']
    response = scoreboard.save(text_to_post,
                               summary='Automatic scoreboard update')
    return response


if __name__=='__main__':
    main()

