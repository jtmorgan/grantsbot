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

import dateutil.parser
import grantsbot_settings
import operator
import output_settings
import profiles
import sys
import templates
import categories

###FUNCTIONS
def makeFeed():
	"""Makes an activity feed for the IdeaLab
	"""
	all_member_list = getMembers()
	all_member_list = tools.addDefaults(all_member_list)
	for member in all_member_list:
		if member['event type'] == "joined":
			pass					
		else:	
			member = getMemberData(member)
# 	print('GOT MEMBER DATA')
# 	print(all_member_list)
	all_member_list = tools.setTimeValues(all_member_list)
# 	print('SET TIME VALUES')
# 	print(all_member_list)
	recently_active = [m for m in all_member_list if m['datetime'] > date_threshold[0]]
	recently_active = tools.dedupeMemberList(recently_active, 'datetime', 'page path')
	#remove pages we don't want to display in the list, like Grants:IdeaLab/Preload
	for r in recently_active:
		if r['page path'] in params['ignored pages']:
			recently_active.remove(r)
	recently_active = recently_active[:6]						
	prepOutput(recently_active)				
	
def getMembers():
	all_member_list = []
	event_types = params['activity']
	for k,v in event_types.iteritems():
		event_type = k
		if v['action'] == 5:
			intro = profiles.Profiles("Grants:IdeaLab/Introductions", id=2101758, settings = params)
			members = intro.getRecentIntros(date_threshold[1])
		elif v['action'] == 1:	
			members = []		
			cat = v['category'] 
			memcat = categories.Categories(cat, namespace = params['main namespace'])
			candidates = memcat.getCatMembers()
			for c in candidates:
				creation_date = dateutil.parser.parse(c['timestamp'])#looks for pages created in specified date range
				if creation_date > date_threshold[0]:
					members.append(c)
				else:
					pass	
		else:
			cat = v['category'] 
			memcat = categories.Categories(cat, namespace = params['main namespace'])
			members = memcat.getCatMembers()						
		for mem in members:
			mem['event type'] = event_type
			mem['action'] = params['activity'][event_type]['action']				
		all_member_list.extend(members)

	return all_member_list					
				
def getMemberData(member):
	profile = profiles.Profiles(member['page path'], id=member['page id'], settings = params) 
	member['title'] = tools.titleFromPath(member['page path'])		
	recent_revs = []
	main_revs = profile.getPageEditInfo(rvend = date_threshold[1],)
	if main_revs:
		recent_revs.extend(main_revs)		
	if member['talkpage id']:
		talk_revs = profile.getPageEditInfo(rvend = date_threshold[1], page = member['talkpage id'])		
		if talk_revs:
			recent_revs.extend(talk_revs)
	if recent_revs:
		participants = len(list(set([x['user'] for x in recent_revs])))
		member['timestamp'] = recent_revs[0]['timestamp']		
		if participants > 2: #get the number of participants
			member['participants'] = participants
			member['action'] = 2
		else: #get the name of the page creator
			recent_revs.sort(key=operator.itemgetter('revid'))			
			member['username'] = recent_revs[0]['user']							
	return member	

def prepOutput(short_member_list):
	output = profiles.Profiles(params['output path'], settings = params) #stupid tocreate a new profile object here.
# 	print(output)
	for m in short_member_list: #inconsistent. i do this earlier in eval_portal
		m['profile'] = output.formatProfile(m) #will this work here?		
	all_profiles = params['header template'] + '\n'.join(m['profile'] for m in short_member_list)
	edit_summ = params['edit summary'] % (params['subtype'] + " " + params['type'])
	output.publishProfile(all_profiles, params['output path'], edit_summ)

###MAIN
param = output_settings.Params()
params = param.getParams(sys.argv[1])
params['type'] = sys.argv[1]
params['subtype'] = sys.argv[2]
tools = profiles.Toolkit()
date_threshold = tools.getSubDate(30)
makeFeed()
