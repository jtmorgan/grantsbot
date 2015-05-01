#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
mbapi
=====

This module contains customized API calls and associated helper methods
for matching.py.
"""

import json
import time

import utils


def get_page_title(pageid, site):
    """Get page title, given page id and a mwclient Site."""
    response = site.api(action='query',
                        prop='info',
                        pageids=pageid)
    title = parse_page_title_response(response)
    print(response)
    return title


def parse_page_title_response(response):
    """Parse the response from mbapi.get_page_title."""
    pagedict = response['query']['pages']
    for page in pagedict:
        title = pagedict[page]['title']
    return title


def get_page_info(title, categories, site):
    """
    Retrieve information on a page, including user information for the
    user who made the first edit, the talk page id, and relevant
    categories the page is in.

    Parameters:
        title       :   a string containing the page title
        categories  :   a list of relevant categories that may be on
                        the page (skills and interests)
        site        :   a mwclient Site object associated with the page

    Returns:
        page_info, a tuple containing the following:
            user            : a string containing the page creator's
                                user name
            userid          : a string containing the page creator's
                                userid
            talkid          : the pageid of the corresponding talk page,
                                if it exists
            page_categories : list of dicts of the form
                                {"ns": 14, "title": "Category:XYZ"} for
                                each category on the page that in the
                                provided list of categories.
    """
    category_string = utils.make_category_string(categories)
    response = site.api(action='query',
                        prop='revisions|info|categories',
                        rvprop='user|userid',
                        rvdir='newer',
                        inprop='talkid',
                        cllimit='max',
                        clcategories=category_string,
                        titles=title,
                        rvlimit=1)
    page_info = parse_page_info_response(response)
    print(response)
    return page_info


def parse_page_info_response(response):
    """Parse the API response for mbapi.get_page_info."""
    pagedict = response['query']['pages']
    for page in pagedict:
        user = pagedict[page]['revisions'][0]['user']
        userid = pagedict[page]['revisions'][0]['userid']
        talkid = pagedict[page].get('talkid')
        page_categories = pagedict[page].get('categories')
    return (user, userid, talkid, page_categories)


def get_new_members(categoryname, site, timelastchecked):
    """Get information on all pages in a given category that have been
    added since a given time.

    Parameters:
        category        :   a string containing the category name,
                            including the 'Category:' prefix
        site            :   mwclient Site object corresponding to the
                            desired category
        timelastchecked :   a MediaWiki-formatted timestamp

    Returns:
        a list of dicts containing information on the category members.

    Handles query continuations automatically.
    """
    recentkwargs = {'action': 'query',
                    'list': 'categorymembers',
                    'cmtitle': categoryname,
                    'cmprop': 'ids|title|timestamp',
                    'cmlimit': 'max',
                    'cmsort': 'timestamp',
                    'cmdir': 'older',
                    'cmend': timelastchecked}
    result = site.api(**recentkwargs)
    newcatmembers = add_new_members_to_list(result, categoryname)

    while True:
        if 'continue' in result:
            newkwargs = recentkwargs.copy()
            for arg in result['continue']:
                newkwargs[arg] = result['continue'][arg]
            result = site.api(**newkwargs)
            newcatmembers = add_new_members_to_list(result, categoryname,
                                                    newcatmembers)
        else:
            break
    print(result)
    return newcatmembers


def add_new_members_to_list(result, categoryname, cat_members=None):
    """Create a list of dicts containing information on each user from
    the mbapi.get_new_members API result.

    Parameters:
        result      :   a dict containing the results of the
                        getnewmembers API query
        categoryname:   a string containing the name of the category
                        that was searched
        catusers    :   a list of dicts with information on category
                        members from earlier queries. Optional,
                        defaults to None.

    Returns:
        a list of dicts containing information on the category members
        in the provided query.
    """
    if cat_members is None:
        cat_members = []
    else:
        pass

    for page in result['query']['categorymembers']:
        userdict = {'profile_id': page['pageid'],
                    'profile_title': page['title'],
                    'cat_time': page['timestamp'],
                    'category': categoryname}
        cat_members.append(userdict)

    return cat_members


def get_all_category_members(category, site):
    """Get information on all members of a given category

    Parameters:
        category:   a string containing the category name, including
                    the 'Category:' prefix
        site    :   mwclient Site object

    Returns:
        a list of dicts containing information on the category members.

    Handles query continuations automatically.
    """
    kwargs = {'action': 'query',
              'list': 'categorymembers',
              'cmtitle': category,
              'cmprop': 'ids|title',
              'cmlimit': 'max'}
    result = site.api(**kwargs)
    cat_members = add_member_info(result)
    while True:
        if 'continue' in result:
            newkwargs = kwargs.copy()
            for arg in result['continue']:
                newkwargs[arg] = result['continue'][arg]
            result = site.api(**newkwargs)
            cat_members = add_member_info(result, cat_members)
        else:
            break
    print(result)
    return cat_members


def add_member_info(result, cat_members=None):
    """Create a list of dicts containing information on each user from
    the get_all_category_members API result.

    Parameters:
        result      :   a dict containing the results of the
                        getallmembers API query
        cat_members :   a list of dicts with information on category
                        members from earlier queries. Optional,
                        defaults to None.
    Returns:
        a list of dicts containing information on the category members
        in the provided query.
    """
    # getting around Python's function/list initialization behavior
    if cat_members is None:
        cat_members = []
    else:
        pass

    for page in result['query']['categorymembers']:
        userdict = {'profileid': page['pageid'], 'profile_title': page['title']}
        cat_members.append(userdict)
    return cat_members
