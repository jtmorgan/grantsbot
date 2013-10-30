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
import dateutil.parser
import grantsbot_settings
import logging
import MySQLdb
import profiles
import output_settings
import re
# import shelve
import sys
import templates
import operator

###FUNCTIONS###
def getMembers(params):
	"""
	Make lists of profiles for resources in a portal.
	"""
	member_list = []
	rows = tools.queryDB(params[params['subtype']]['query'])
	member_list = [{'timestamp' : row[0], 'page path' : params[params['subtype']]['namespace'] + row[1], 'page id' : row[2],} for row in rows]		
	member_list = tools.addDefaults(member_list)
	for member in member_list:
		member = getMemberData(member)
	prepOutput(member_list)		

def makeFeed(input_params, params):
	"""
	Make an activity feed for a portal.
	"""
	tools = profiles.Toolkit()
	member_list = getMembers(input_params, params, tools)
	i = 1
	for member in member_list:
		member['item'] = i	
		member = getMemberData(member, input_params, params, tools)
		i += 1
	prepOutput(member_list, input_params, params, tools)	
			
def getMembers(input_params, params, tools = False):

			rows = tools.queryDB(params[input_params[2]]['query'])
			member_list = [{'timestamp' : row[0], 'page path' : params[input_params[2]]['namespace'] + row[1], 'page id' : row[2],} for row in rows]	
		else: 
			pass
	elif input_params[0] == 'feed':
		member_list = assembleFeedMembers(input_params, params, tools)
	elif input_params[0] == 'gallery':
		pass
	else:
		pass		
	member_list = tools.addDefaults(member_list)
	return member_list	

def assembleFeedMembers(input_params, params, tools):
	member_list = []
	if input_params[1] == 'idealab':
		pass
	elif input_params[1] == 'evalportal':
		queries = params[input_params[2]]
		for k, v in queries.iteritems():
			rows = tools.queryDB(v['query'])
			if v['action'] == 2: 
				members = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'page path' : v['namespace'] + row[2], 'action' : v['action'], 'title' : tools.titleFromComment(row[3])} for row in rows]
			else:
				members = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'page path' : v['namespace'] + row[2], 'action' : v['action'], 'title' : tools.titleFromPath(row[2])} for row in rows]
			member_list.extend(members)
	else:
		pass
	return member_list				

				
def getMemberData(member, input_params, params, tools = False):
	profile = profiles.Profiles(member['page path'], input_params[0], id=member['page id'], params = params) 
	member = profile.setTimeValues(member, input_params)
	if member['username']:
		member['username'] = tools.formatSummaries(member['username']) #sloppy, but better. Strips anything that looks like markup from username.	
	else:
		pass	
	if input_params[0] == 'guide': #necessary?	
		member['title'] = tools.titleFromPath(member['page path'])	#new function to get title from path
		infobox = profile.getPageText(0)
		member = profile.scrapeInfobox(member, infobox)
	else:
		pass
	member['profile'] = profile.formatProfile(input_params, member)				
	return member		

def prepOutput(member_list, input_params, params, tools):
	member_list = tools.dedupeMemberList(member_list, 'datetime', 'page path') #not the ideal place for this
	member_list.sort(key=operator.itemgetter('datetime'), reverse=True) #abstract this?
	###MOVE THIS IF###
	if input_params[2] == 'new': #won't work yet. need to do this earlier
		member_list = member_list[0:10] #Do this in an earlier step? also, 'new' is no longer a valid subtype!
	else:
		pass				
	all_profiles = params['header template'] + '\n'.join(member['profile'] for member in member_list)
# 	print all_profiles
	if 'subpage' in params[input_params[2]]:
		sb_page = params[input_params[2]]['subpage']
	else: sb_page = ""
	if 'output section' in params[input_params[2]]:
		edit_sec = params[input_params[2]]['output section']
	else: edit_sec = ""			
	edit_summ = params['edit summary'] % (input_params[1] + " " + input_params[0])
	output = profiles.Profiles(params['output path'], profile_type) #stupid tocreate a new profile object here.
	output.publishProfile(all_profiles, params['output path'], edit_summ, sb_page, edit_sec)
	

###MAIN###
input_params = {'type' : sys.argv[1], 'subtype' : sys.argv[2]}
param = output_settings.Params()
params = param.getParams(input_params['type'])
tools = profiles.Toolkit()
for k,v in input_params.iteritems():
	params[k] = v
getMembers(params)	
# if input_params['type'] == "guide":
# 	makeGuide(params)
# elif input_params['type'] == "feed":
# 	makeFeed(params)
# elif input_params['type'] == "gallery":
# 	makeGallery(params)
# else: 
# 	print "unrecognized profile type. Options are gallery, guide and feed."		
