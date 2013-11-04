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

###FUNCTIONS###
def makeGuide():
	"""
	Make lists of profiles for resources in a portal.
	"""
	member_list = getMembers()
	for member in member_list:
		member = getMemberData(member)
	member_list = tools.setTimeValues(member_list)			
	member_list = tools.addDefaults(member_list)
	member_list.sort(key=operator.itemgetter('datetime'), reverse=True)	
	if params['subtype'] == "new":
		member_list = member_list[:10]		
# 	print member_list		
	prepOutput(member_list)				
	
def getMembers():
	cat = params[params['subtype']]['category']
	memcat = categories.Categories(cat, namespace = params['main namespace']) #not sure if namespace is optional in categories?
	member_list = memcat.getCatMembers()
	for member in member_list:
		member['title'] = tools.titleFromPath(member['page path'])	
	return member_list	
		
def getMemberData(member):
	profile = profiles.Profiles(member['page path'], id=member['page id'], settings = params) 
	infobox = profile.getPageText(0) #zero is the top section
	member = profile.scrapeInfobox(member, infobox, redict = params['infobox params'])
	member['timestamp'] = profile.getPageFirstOrLatest()			
	return member		

def prepOutput(member_list):
	output = profiles.Profiles(params['output path'], settings = params) #stupid tocreate a new profile object here.
	for member in member_list: #inconsistent. i do this earlier in eval_portal
		if (member['username'] and "]]" not in member['username']):
			member['username'] = member['username'] + "]]" #sloppy. makes a wikilink of username
		else: pass
		member['profile'] = output.formatProfile(member) #will this work here?		
	all_profiles = params['header template'] + '\n'.join(member['profile'] for member in member_list)
	edit_summ = params['edit summary'] % (params['subtype'] + " " + params['type'])
	output.publishProfile(all_profiles, params['output path'], edit_summ, sb_page = params[params['subtype']]['subpage'])
	

###MAIN###
param = output_settings.Params()
params = param.getParams(sys.argv[1])
params['type'] = sys.argv[1]
params['subtype'] = sys.argv[2]
tools = profiles.Toolkit()
makeGuide()	

