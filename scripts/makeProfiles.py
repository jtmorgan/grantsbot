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
from datetime import datetime
import grantsbot_settings
import logging
import profiles
import re
import shelve
import sys

logging.basicConfig(filename= grantsbot_settings.logs + 'moves.log', level=logging.INFO)
curtime = str(datetime.utcnow())
cat_title = sys.argv[1] #you specify the target category at the command line
cat_type = sys.argv[2] #you specify the kind of members you want at the command line
profile_type = sys.argv[3] #you specify the kind of profile you want at the command line

	
###FUNCTIONS###
def makeProfiles():
	"""
	create profiles for IdeaLab ideas.
	"""
	profile_elements = {'participants' : '|participants', 'summary' : '|summary'}
	category = categories.Categories(cat_title, cat_type, 200)
	member_list = category.getCatMembers()
	member_list = member_list[0:10] #use sublist for quicker tests
	for member in member_list:
		path = member['page_path']
		page = profiles.Profiles(path, profile_type) #needs to accept full paths
		member['infobox'] = page.getPageText(0) #infoboxes are always in the top section
		infobox = member['infobox']
		for line in infobox.split('\n'):
# 			print line
			for k, v in profile_elements.iteritems():
# 				print k
# 				print v
				if line.startswith(v, 0, len(v)):
					try:
						m = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
# 						print m
						member[k] = m
					except:
						print "nope"	
		print member['participants']
		print member['summary']
		
			
		

# 	profile_page.publishProfiles(plist_sorted)
	
###MAIN###
makeProfiles()	