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
import operator
import output_settings
import profiles
import sys
import templates

###FUNCTIONS###
def makeGuide(params):
	"""
	Make lists of profiles for resources in a portal.
	"""
	member_list = getMembers()
	member_list.sort(key=operator.itemgetter('datetime'), reverse=True)		
	for member in member_list:
		member = getMemberData(member)
	prepOutput(member_list)				
	
def getMembers():
	member_list = []
	rows = tools.queryDB(params[params['subtype']]['query'])
	members = [{'timestamp' : row[0], 'page path' : params[params['subtype']]['namespace'] + row[1], 'page id' : row[2], 'title' : tools.titleFromPath(row[1])} for row in rows]	
	member_list.extend(members)
	member_list = tools.addDefaults(member_list)
	member_list = tools.setTimeValues(member_list)	
	return member_list	
		
def getMemberData(member):
	profile = profiles.Profiles(member['page path'], id=member['page id'], settings = params) 
	infobox = profile.getPageText(section = 0) #zero is the top section
	member = profile.scrapeInfobox(member, infobox)
	member['profile'] = profile.formatProfile(member)				
	return member		

def prepOutput(member_list):			
	all_profiles = params[params['subtype']]['header template'] + '\n'.join(member['profile'] for member in member_list)
	edit_summ = params['edit summary'] % (params['subtype'] + " " + params['type'])
	output = profiles.Profiles(params['output path'], params['type']) #stupid tocreate a new profile object here.
	output.publishProfile(all_profiles, params['output path'], edit_summ, sb_page = params[params['subtype']]['subpage'], edit_sec = params['output section'])
	

###MAIN###
param = output_settings.Params()
params = param.getParams(sys.argv[1])
params['type'] = sys.argv[1]
params['subtype'] = sys.argv[2]
tools = profiles.Toolkit()
makeGuide(params)	

