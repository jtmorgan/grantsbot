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

from datetime import datetime
import logging
import profiles
import grantsbot_settings
import sys

logging.basicConfig(filename= grantsbot_settings.logs + 'moves.log', level=logging.INFO)
curtime = str(datetime.utcnow())
profile_type = sys.argv[1] #you specify the profile type at the command line
page_path = sys.argv[2] #you specify the target page name at the command line

###FUNCTIONS###
def rankProfiles(): #needs to be made agnostic, so that it will rank both idea profiles and people profiles
	"""
	rank IdeaLab profiles by number of recent edits.
	"""
	profile_page = profiles.Profiles(page_path, profile_type)
	profile_list = profile_page.getPageSectionData()
	# profile_list = profile_list[0:2] #use sublist for quicker tests
	for profile in profile_list:
		profile['text'] = profile_page.getPageText(profile['profile_index'])
		main_edits = profile_page.getUserRecentEdits(profile['username'], 200)
		talk_edits = profile_page.getUserRecentEdits(profile['username'], 201)
		profile['edits'] = main_edits + talk_edits
	plist_sorted = sorted(profile_list, key=lambda item: item['edits'], reverse = True)
	plist_text = {'profiles' :'\n'.join([x['text'] for x in plist_sorted])} #join 'em all together
	formatted_profiles = profile_page.formatProfile(plist_text)
	profile_page.publishProfile(formatted_profiles, "**TeSt** Reordering the IdeaLab profiles, putting more recently active collaborators at the top")
	logging.info('Reordered IdeaLab profiles at ' + curtime)

###MAIN###
if profile_type == "people":
	rankProfiles()
else:
	print "sorry, we're not set up to work with " + profile_type + "profiles yet!"