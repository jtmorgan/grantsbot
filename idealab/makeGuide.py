#! /usr/bin/python2.7

# Copyright 2013 Jtmorgan

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import grantsbot_settings
import categories
import operator
import output_settings
import profiles
import sys
import templates

def makeGuide():
    """
    Make lists of profiles for resources in a portal.
    """
    member_list = getMembers()
    member_list = tools.excludeSubpages(member_list, 'page path') #excluding translated subpages
    for member in member_list:
        member = getMemberData(member)
    member_list = tools.setTimeValues(member_list, val = params[params['subtype']]['time value'])
    member_list = tools.addDefaults(member_list)
    member_list.sort(key=operator.itemgetter('datetime'), reverse=True)
    if params['subtype'] == 'new':
        member_list = member_list[:5]
    prepOutput(member_list)

def multicat(catlist1, catlist2):
    catlist3 = []
    for x in catlist1:
        for y in catlist2:
            if x['page path'] in y.values():
                catlist3.append(x)
    return catlist3

def getMembers():
    cats = params[params['subtype']]['categories']
    member_list = []
    if (params['type'] == 'idealab_guide' and params['subtype'] == 'inspire-draft'):
        proj_draft_cat = categories.Categories('Project/Proposals/IdeaLab', namespace = params['main namespace'])
        proj_cat_list = proj_draft_cat.getCatMembers() #gets all members of project/proposals/draft
        rapid_draft_cat = categories.Categories('Rapid/Proposals/IdeaLab', namespace = params['main namespace'])
        rapid_cat_list = rapid_draft_cat.getCatMembers() #gets all members of rapid/proposals/draft
        inspire_draft_cat = categories.Categories('IdeaLab/Ideas/Inspire/Knowledge_networks', namespace = params['main namespace'])
        inspire_cat_list = inspire_draft_cat.getCatMembers() #gets all inspire ideas for the current campaign
        member_list.extend(multicat(rapid_cat_list, inspire_cat_list))
        member_list.extend(multicat(proj_cat_list, inspire_cat_list))
    else:
        for cat in cats:
            memcat = categories.Categories(cat, namespace = params['main namespace']) #not sure if namespace is optional in categories?
            cat_list = memcat.getCatMembers()
            member_list.extend(cat_list)
    member_list = tools.dedupeMemberList(member_list, 'timestamp', 'page id')
    if params['type'] == 'pattern_guide':
        member_list = learningPatternsHack(member_list)
    for member in member_list:
        member['title'] = tools.titleFromPath(member['page path'])
#                 print(member['page path'])
    return member_list

def learningPatternsHack(member_list):
    #a hack to prune the LP list
    #not using 'ignored pages' because there are a lot of pages to ignore
    return [m for m in member_list if m['page path'].startswith('Learning patterns')]

def getMemberData(member):
    profile = profiles.Profiles(member['page path'], id=member['page id'], settings = params)
    infobox = profile.getPageText(0) #zero is the top section
    member = profile.scrapeInfobox(member, infobox, redict = params['infobox params'])
    revs = []
    main_revs = profile.getPageEditInfo()
    revs.extend(main_revs)
    if member['talkpage id']:
        talk_revs = profile.getPageEditInfo(page = member['talkpage id'])
        if talk_revs:
            revs.extend(talk_revs)
    revs.sort(key=operator.itemgetter('revid'), reverse=True)
    member['timestamp'] = revs[0]['timestamp']
    revs.sort(key=operator.itemgetter('revid'), reverse=False)  #this doesn't seem to be working
    member['username'] = "[[User:" + revs[0]['user'] + "]]"
    member['created'] = revs[0]['timestamp']
    if params['formatted fields']:
        for field in params['formatted fields']: #do I need the 'if' above this line?
            try:
                member[field] = tools.formatSummaries(member[field])
            except:
                pass
    return member

def prepOutput(member_list):
    output = profiles.Profiles(params['output path'], settings = params)
    for member in member_list:
        member['profile'] = output.formatProfile(member)
#         print(member)
    all_profiles = params['header template'] + '\n'.join(member['profile'] for member in member_list)
    edit_summ = params['edit summary'] % (params['type'] + " " + params['subtype'])
    output.publishProfile(all_profiles, params['output path'], edit_summ, sb_page = params[params['subtype']]['subpage'])


if __name__ == "__main__":
    param = output_settings.Params()
    params = param.getParams(sys.argv[1])
    params['type'] = sys.argv[1]
    params['subtype'] = sys.argv[2]
    tools = profiles.Toolkit()
    makeGuide()

