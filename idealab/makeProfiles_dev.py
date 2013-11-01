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
import output_params
import re
# import shelve
import sys
import templates
import operator

logging.basicConfig(filename = grantsbot_settings.logs + 'makes.log', level = logging.INFO)
curtime = str(datetime.utcnow())

###FUNCTIONS###
def makeGuide(input_params, params):
	"""
	Make lists of profiles for resources in a portal.
	"""
	tools = profiles.Toolkit()
	member_list = getMembers(input_params, params, tools)
	for member in member_list:
		member = getMemberData(member, input_params, params, tools)
	prepOutput(member_list, input_params, params, tools)	

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
		
def makeGallery(input_params, params):
	"""
	Make a featured content gallery for a portal.
	"""
	member_list = getMembers(profile_type, profile_subtype, params, tools)
	for member in member_list:
		member = getMemberData(member, profile_type, profile_subtype, params, tools) #new method
	prepareOutput(member_list, profile_type, profile_subtype, params, tools)	
	
def getMembers(input_params, params, tools = False):
	if input_params[0] == 'guide':
		if input_params[1] == "idealab": 
			cat = params[input_params[2]]['category'] #e.g. 'IEG/Drafts'
			category = categories.Categories(cat)
			member_list = category.getCatMembers()
		elif input_params[1] == "evalportal":
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
	# members = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'page path' : entry['namespace'] + row[2], 'action' : params['pattern']['action']} for row in rows]
# 	# 	#get recent endorsements
# 		rows = tools.queryDB('recent endorsements')
# 		endorsments = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'page path' : "Grants:" + row[2], 'action' : params['endorse']['action']} for row in rows]	
# 	# 	#get recently-created profiles
# 		rows = tools.queryDB('recent intros')
# 		intros = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'action' : params['people']['action'], 'page path' : params['people']['subpage'], 'title' : ''} for row in rows]
# 	# get recent questions	
# 		rows = tools.queryDB('recent questions')
# 		questions = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'page path' :  params['question']['subpage'], 'action' : params['question']['action']} for row in rows]	
# 		member_list.extend(patterns + endorsments + intros + questions)
# 		for m in member_list:
# 			if m['action'] != 5:
# 				m['title'] = re.search('([^/]+$)', m['page path']).group(1)
# 				m['title'] = m['title'].replace("_", " ")
# 			dates = tools.formatPrettyDate(m['timestamp'], "mysql") #test this
# 			m['datetime'] = dates[0]
# 			m['time'] = dates[1]
# 	else:
# 		pass
# 	return member_list
				
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
	

#for feed:
#get member lists (multiple passes through either API or DB)
#assign action (one per pass)
#scrape infobox (do after action) getrecenteditinfo, getsubdate, 
#fix datetime added stuff
def getEvalFeed(params, profile_type, tools):
	member_list = []
	# #get recently created patterns
	rows = tools.queryDB('recent patterns')
	patterns = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'page path' : "Grants:" + row[2], 'action' : params['pattern']['action']} for row in rows]
# 	#get recent endorsements
	rows = tools.queryDB('recent endorsements')
	endorsments = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'page path' : "Grants:" + row[2], 'action' : params['endorse']['action']} for row in rows]	
# 	#get recently-created profiles
	rows = tools.queryDB('recent intros')
	intros = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'action' : params['people']['action'], 'page path' : params['people']['subpage'], 'title' : ''} for row in rows]
# get recent questions	
	rows = tools.queryDB('recent questions')
	questions = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'page path' :  params['question']['subpage'], 'action' : params['question']['action']} for row in rows]	
	member_list.extend(patterns + endorsments + intros + questions)
	for m in member_list:
		if m['action'] != 5:
			m['title'] = re.search('([^/]+$)', m['page path']).group(1)
			m['title'] = m['title'].replace("_", " ")
		dates = tools.formatPrettyDate(m['timestamp'], "mysql") #test this
		m['datetime'] = dates[0]
		m['time'] = dates[1]
	return member_list	



def makeIdeaLabFeed(params, profile_type, tools, all_member_list, subtype_list, date_since):
	for subtype in subtype_list:
		cat = params[subtype]['category']
		category = categories.Categories(cat, 200) #namespace redundancy
		member_list = category.getCatMembers()
		for member in member_list:
			member['subtype'] = subtype
			member['action'] = params[member['subtype']]['action'] #put this in cat class
		all_member_list.extend(member_list)
	for member in all_member_list:
		profile = profiles.Profiles(member['page path'], profile_type, member['page id'])
		member['title'] = re.search('([^/]+$)', member['page path']).group(1)
		member['timestamp'] = member['datetime added'] #fix this!!!
		dates = tools.formatPrettyDate(member['timestamp'], "api") #test this. also, the type should be a param
		member['datetime'] = dates[0]
		member['time'] = dates[1]		
# 		member['time'] = tools.parseISOtime(member['datetime added']) #should put this in cat class
		recent_editors = profile.getPageRecentEditInfo(date_since, pages=(member['page id'], member['talkpage id'],))
		if len(recent_editors) > 3:
			member['participants'] = len(recent_editors)
			member['action'] = 2
			member['creator'] = ""
			member['time'] = tools.getSubDate(0, "pretty") #we use today's date for this kind of item
		else:
			member['participants'] = ""
			infobox = profile.getPageText(0) #infoboxes are always in the top section
			creator_re = params['creator']
			member['creator'] = ""
			for line in infobox.split('\n'):
				if re.search(creator_re, line):
					try:
						member['creator'] = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1).strip()
						break #does this break work? Do I need it elsewhere?
					except:
						logging.info("Could not get profile creator for " + member['page path'] + " " + curtime)
				else:
					pass
	all_member_list = [x for x in all_member_list if len(x.get('creator')) > 0 or x.get('action') == 2] #only keep ones with a creator or more than two participants
	return all_member_list


###MAIN###
profile_type = sys.argv[1] #the type of profiles you're making. "guide", "gallery" and "feed". 
portal = sys.argv[2] #the portal you're making them for. "idealab" "evalportal"
profile_subtype = sys.argv[3] #e.g. "pattern", "participants"
input_params = [profile_type, portal, profile_subtype]
param = output_params.Params()
params = param.getParams(input_params[0], input_params[1])
if input_params[0] == "guide":
	makeGuide(input_params, params)
elif input_params[0] == "feed":
	makeFeed(input_params, params)
elif input_params[0] == "gallery":
	makeGallery(input_params, params)
else: 
	print "unrecognized profile type. Options are gallery, guide and feed."		



# guide_profile_types = ['idea_profile', 'evaluation_resource_profile',]
# gallery_profile_types = ['featured_idea', 'featured_evaluation_resource',]
# feed_profile_types = ['idealab_activity_feed', 'evaluation_activity_feed',] #make sure names are consistent
