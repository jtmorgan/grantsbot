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

import profiles
import grantsbot_settings
import output_settings
import sys

###FUNCTIONS###
def rankProfiles():
	"""
	rank IdeaLab profiles by number of recent edits.
	"""
	profile_page = profiles.Profiles(params['output path'], params['output page id'], params)
	profile_list = profile_page.getPageSectionData()
	for profile in profile_list:
		profile['title'].encode("utf8")#so redundant!
		profile['text'] = profile_page.getPageText(profile['index'])
		main_edits = profile_page.getUserRecentEditInfo(profile['title'], params['main namespace'])
		talk_edits = profile_page.getUserRecentEditInfo(profile['title'], params['talk namespace'])
		profile['edits'] = main_edits + talk_edits		
	plist_sorted = sorted(profile_list, key=lambda item: item['edits'], reverse = True)
	plist_text = {'profiles' :'\n\n'.join([x['text'] for x in plist_sorted])} 
	formatted_profiles = profile_page.formatProfile(plist_text)
	edit_summ = params['edit summary'] % (params['type'],)
	profile_page.publishProfile(formatted_profiles, params['output path'], edit_summ)

###MAIN###
param = output_settings.Params()
params = param.getParams(sys.argv[1])
params['type'] = sys.argv[1]
rankProfiles()
