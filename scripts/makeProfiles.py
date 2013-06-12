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


import categories
import dateutil.parser
from datetime import datetime
import grantsbot_settings
import logging
import profiles
import re
import shelve
import sys

logging.basicConfig(filename= grantsbot_settings.logs + 'makes.log', level=logging.INFO)
curtime = str(datetime.utcnow())
cat_title = sys.argv[1] #you specify the target category at the command line
cat_type = sys.argv[2] #you specify the kind of members you want at the command line
profile_type = sys.argv[3] #you specify the kind of profile you want at the command line


###FUNCTIONS###
def makeProfiles():
	"""
	create profiles for IdeaLab ideas.
	"""
	profile_elements = {'summary' : '|summary'}
	category = categories.Categories(cat_title, cat_type, 200)
	member_list = category.getCatMembers()
	member_list = member_list[0:4] #use sublist for quicker tests
	profiles_formattedx = [] #this is a crappy workaround. fix it.
	for member in member_list:
		datetimefm = dateutil.parser.parse(member['datetime_added'])
		datetimefm = datetimefm.strftime('%x')
		member['datetime_added'] = datetimefm
		page = profiles.Profiles(member['page_path'], profile_type) #needs to accept full paths
		touched = page.getPageInfo('touched')
# 		print touched
		member['time'] = dateutil.parser.parse(touched).strftime('%x')
		infobox = page.getPageText(0) #infoboxes are always in the top section
		for line in infobox.split('\n'):
			for k, v in profile_elements.iteritems():
				if line.startswith(v, 0, len(v)):
					try:
						m = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
						member[k] = m
					except:
						print "nope"

		member[profile_type] = re.search('([^/]+$)', member['page_path']).group(1)
# 		print member ['idea']
		profile_formatted = page.formatProfile(member)
# 		print profile_formatted
		profiles_formattedx.append(profile_formatted)
	profiles_textx = '\n\n'.join(x for x in profiles_formattedx)
	print profiles_textx
	logging.info('Made some ' + profile_type + 'profiles at ' + curtime)





# 	profile_page.publishProfiles(plist_sorted)

###MAIN###
makeProfiles() #need to include some validation so that it only tries of the kind of profile you specified is listed somewhere.