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
import output_settings
import profiles
from random import shuffle
import sys
import templates

###FUNCTIONS
def makeGallery():
    """
    Makes featured profiles for IdeaLab galleries.
    """
    if params['subtype'] in ['intro', 'new_idea', 'ieg_draft', 'participants_wanted']:
        featured_list = getFeaturedProfiles()
    else:
        sys.exit("unrecognized featured content type " + params['subtype']) 
    prepOutput(featured_list)               

def getFeaturedProfiles():
    """
    Gets info about the top-billed profiles in a guide.
    """
    featured_list = []
    profile_page = profiles.Profiles(params[params['subtype']]['input page path'], params[params['subtype']]['input page id'], params)
    profile_list = profile_page.getPageSectionData(level = params[params['subtype']]['profile toclevel'])
    for profile in profile_list:
#         print profile
        text = profile_page.getPageText(profile['index'])
        profile = profile_page.scrapeInfobox(profile, text)
        if len(profile['summary']) > 1 and len(profile['image']) > 1:
            profile['action'] = params[params['subtype']]['action']
            profile['summary'] = tools.formatSummaries(profile['summary'])  
            featured_list.append(profile)
    shuffle(featured_list)
    featured_list = featured_list[:params[params['subtype']]['number featured']]
    return featured_list        
    
def prepOutput(featured_list):
    first_subpage = params[params['subtype']]['first subpage']
    number_featured = params[params['subtype']]['number featured']  
    featured_list = tools.addDefaults(featured_list)            
    output = profiles.Profiles(params[params['subtype']]['output path'], settings = params) #stupid tocreate a new profile object here. and stupid to re-specify the path below
    i = first_subpage
    for f in featured_list:
        if i <= first_subpage + (number_featured - 1):
            f['profile'] = output.formatProfile(f)
            f['profile'] = params['header template'] + '\n' + f['profile']
            edit_summ = params['edit summary'] % (params['subtype'] + " " + params['type'])
            output.publishProfile(f['profile'], params[params['subtype']]['output path'], edit_summ, sb_page = i)
            i += 1
        else:
            break   
            
if __name__ == "__main__":
    param = output_settings.Params()
    params = param.getParams(sys.argv[1])
    params['type'] = sys.argv[1]
    params['subtype'] = sys.argv[2]
    tools = profiles.Toolkit()
    makeGallery()   