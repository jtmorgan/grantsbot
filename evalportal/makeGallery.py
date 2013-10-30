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
from collections import OrderedDict
# from operator import itemgetter
import output_settings
import profiles
import sys
import templates

###FUNCTIONS###
def makeGallery(params):
	"""
	Make lists of profiles for resources in a portal.
	"""
	member_list = getMembers()
	member_list.sort(key=operator.itemgetter('action', 'datetime'), reverse = True)	
	i = member_list[0]['action']
	counter = 0
	j = 1
	new_list = [] #this is so slop. need to not be creating a new list here.
	for member in member_list:
		if member['action'] == i:
			if counter < params['number featured']:
				member['item'] = j
				member = getMemberData(member)#get some stuff about the member
				counter += 1
				prepOutput([member,], j)	
				j += 1							
			else:
				pass	
		elif member['action'] < i:
			i = member['action']
			member['item'] = j
			member = getMemberData(member)
			counter = 1	
			prepOutput([member,], j)				
			j += 1			
		else:
			break 	
	
def getMembers(): #no page id for activity
	"""Returns list already sorted"""
	member_list = []
	queries = params[params['subtype']]
	for k, v in queries.iteritems():
		rows = tools.queryDB(v['query'])
		if v['action'] == 4: #should make actions consistent across different templates 
			members = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'page path' : v['namespace'] + row[2], 'action' : v['action'], 'title' : tools.titleFromComment(row[3])} for row in rows]
		elif v['action'] == 5:
			members = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'page path' : v['namespace'] + row[2], 'action' : v['action'], 'title' : row[0].decode("utf8"),} for row in rows]			
		else:
			members = [{'timestamp' : row[0], 'page path' : v['namespace'] + row[1], 'page id' : row[2], 'action' : v['action'], 'title' : tools.titleFromPath(row[1])} for row in rows] #very inconsistent with the other queries
		member_list.extend(members)	
	member_list = tools.addDefaults(member_list)
	member_list = tools.setTimeValues(member_list)
	return member_list		
		
def getMemberData(member):
	member['username'] = tools.formatSummaries(member['username']) #Strips anything that looks like markup.	
	if member['action'] == 1:
		profile = profiles.Profiles(member['page path'], id = member['page id'], settings = params) 	
		text = profile.getPageText(0) #zero is the top section
		member = profile.scrapeInfobox(member, text, params['infobox params'])
		member['profile'] = profile.formatProfile(member)			
	else:
		profile = profiles.Profiles(member['page path'], settings = params) 	
		member['profile'] = profile.formatProfile(member)
	return member		

def prepOutput(member_list, j):
	all_profiles = params['header template'] + '\n'.join(member['profile'] for member in member_list) #different from guide
	edit_summ = params['edit summary'] % (params['subtype'] + " " + params['type'])
	output = profiles.Profiles(params['output path'], params['type']) #stupid tocreate a new profile object here?
	output.publishProfile(all_profiles, params['output path'] + params['sub page'], edit_summ, sb_page = j)
	

###MAIN###
param = output_settings.Params()
params = param.getParams(sys.argv[1])
params['type'] = sys.argv[1]
params['subtype'] = sys.argv[2]
tools = profiles.Toolkit()
makeGallery(params)	
