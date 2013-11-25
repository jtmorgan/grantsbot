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
import categories

###FUNCTIONS
def makeGallery():
	"""Makes featured profiles for idealab galleries.
	"""
	if params['subtype'] == 'intro':
		featured_list = getIntros()
	elif params['subtype'] == 'idea':
		####
	elif params['subtype'] == 'ieg':
		#### 
	elif params['subtype'] == 'participants':		
		
	prepOutput(featured_list)				

def getIntros():
	"""
	Gets info about the top-billed participants on the intros page.
	"""
	featured_list = []
	profile_page = profiles.Profiles(params[params['subtype']]['input page path'], params[params['subtype']]['input page id'], params)
	profile_list = profile_page.getPageSectionData(level = params[params['subtype']]['profile toclevel'])
	profile_list = profile_list[:6]
	for profile in profile_list:
		text = profile_page.getPageText(profile['index'])
		profile = profile_page.scrapeInfobox(profile, text)
		if (profile['summary'] and profile['name']):
			profile['action'] = params[params['subtype']]['action']
			profile['summary'] = tools.formatSummaries(profile['summary'])
			profile['username'] = "User:" + profile['title'] 
			del profile['title'] #title is used for featured ideas, in a different param
			featured_list.append(profile)
	
	return featured_list		



def prepOutput(featured_list):
	i = 1
	featured_list = tools.addDefaults(featured_list)       		
	output = profiles.Profiles(params[params['subtype']]['output path'], settings = params) #stupid tocreate a new profile object here. and stupid to re-specify the path below
	for f in featured_list:
		if i <= params['number featured']:
			f['profile'] = output.formatProfile(f)
			f['profile'] = params['header template'] + '\n' + f['profile']
			edit_summ = params['edit summary'] % (params['subtype'] + " " + params['type'])
			output.publishProfile(f['profile'], params[params['subtype']]['output path'], edit_summ, sb_page = i)
			i += 1
		else:
			break	

###MAIN
param = output_settings.Params()
params = param.getParams(sys.argv[1])
params['type'] = sys.argv[1]
params['subtype'] = sys.argv[2]
tools = profiles.Toolkit()
makeGallery()	

###CRAPLINE
# def getMembers():
# 	all_member_list = []
# 	event_types = params['featured']
# 	for k,v in event_types.iteritems():
# 		profile_type = k
# 		if v['action'] == 1:
# 			cat = v['category'] 
# 			memcat = categories.Categories(cat, namespace = params['main namespace'])
# 			members = memcat.getCatMembers()
# 			for mem in members:
# 				mem['profile type'] = profile_type
# 				mem['action'] = params['featured'][event_type]['action']
# 			all_member_list.extend(members)
# 		elif v['action'] == 5:	
# 			intro = profiles.Profiles("Grants:IdeaLab/Introductions", id=2101758, settings = params)
# 			recent_intros = intro.getRecentIntros(date_threshold)
# 			for i in recent_intros:
# 				i['profile type'] = profile_type
# 			all_member_list.extend(recent_intros)
# 		else:
# 			pass	
# 	return all_member_list					
				
# def getMemberData(member):
# 	profile = profiles.Profiles(member['page path'], id=member['page id'], settings = params) 
# 	member['title'] = tools.titleFromPath(member['page path'])		
# 	if member['event type'] == "joined":
# 		pass
# 	else:	
# 		recent_revs = []
# 		main_revs = profile.getPageEditInfo(rvend = date_threshold[1],)
# 		if main_revs:
# 			recent_revs.extend(main_revs)		
# 		if member['talkpage id']:
# 			talk_revs = profile.getPageEditInfo(rvend = date_threshold[1], page = member['talkpage id'])		
# 			if talk_revs:
# 				recent_revs.extend(talk_revs)
# 		if recent_revs:
# 			member['participants'] = len(list(set([x['user'] for x in recent_revs])))		
# 			if member['participants'] > 2:
# 				member['action'] = 2
# 				recent_revs.sort(key=operator.itemgetter('revid'), reverse=True)			
# 				member['timestamp'] = recent_revs[0]['timestamp']				
# 	return member	