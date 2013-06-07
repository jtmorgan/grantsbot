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

import logging
import profiles
import grantsbot_settings
from datetime import datetime

logging.basicConfig(filename= grantsbot_settings.logs + 'moves.log', level=logging.INFO)
curtime = str(datetime.utcnow())
page_title = "IdeaLab/Introductions"
	
###FUNCTIONS###
def makeProfiles():
	"""
	create profiles for IdeaLab ideas.
	"""

	profile_page = profiles.Profiles(page_title)
	profile_list = profile_page.getPageSectionData()
	# profile_list = profile_list[0:2] #use sublist for quicker tests
	for profile in profile_list:
		profile['text'] = profile_page.getPageText(profile['profile_index'])
		main_edits = profile_page.getUserRecentEdits(profile['username'], 200)
		talk_edits = profile_page.getUserRecentEdits(profile['username'], 201)
		profile['edits'] = main_edits + talk_edits
	plist_sorted = sorted(profile_list, key=lambda item: item['edits'], reverse = True)
	profile_page.publishProfiles(plist_sorted)
	logging.info('Reordered IdeaLab profiles at ' + curtime)
	
###MAIN###
makeProfiles()	