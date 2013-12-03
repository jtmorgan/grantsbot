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
def makeFeed(params):
	"""
	Make lists of profiles for resources in a portal.
	"""
	member_list = getMembers()
	member_list.sort(key=operator.itemgetter('datetime'), reverse=True)	
	member_list = member_list[0:6]	
	i= 1
	for member in member_list:
		member = getMemberData(member, i)
		i += 1
	prepOutput(member_list)				
	
def getMembers(): #no page id for activity
	"""Returns list already sorted"""
	member_list = []
	queries = params[params['subtype']]
	for k, v in queries.iteritems():
		rows = tools.queryDB(v['query'])
		if v['action'] == 2: 
			members = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'page path' : v['namespace'] + row[2], 'action' : v['action'], 'title' : tools.titleFromComment(row[3])} for row in rows]
		elif v['action'] == 5:
			members = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'page path' : v['namespace'] + row[2] + "#" + row[0].decode("utf8"), 'action' : v['action'], 'title' : 'the Evaluation portal'} for row in rows]			
		else:
			members = [{'username' : row[0].decode("utf8"), 'timestamp' : row[1], 'page path' : v['namespace'] + row[2], 'action' : v['action'], 'title' : tools.titleFromPath(row[2])} for row in rows]
		member_list.extend(members)	
	member_list = tools.addDefaults(member_list)
	member_list = tools.setTimeValues(member_list)
	return member_list		
		
def getMemberData(member, i):
	member['username'] = tools.formatSummaries(member['username']) #Strips anything that looks like markup.	
	member['item'] = i
	profile = profiles.Profiles(member['page path'], settings = params) 	
	member['profile'] = profile.formatProfile(member)
	return member		

def prepOutput(member_list):
	all_profiles = params['header template'] + '\n'.join(member['profile'] for member in member_list) #different from guide
	edit_summ = params['edit summary'] % (params['subtype'] + " " + params['type'])
	output = profiles.Profiles(params['output path'], params['type']) #stupid tocreate a new profile object here?
	output.publishProfile(all_profiles, params['output path'], edit_summ, edit_sec = params['output section'])
	

###MAIN###
param = output_settings.Params()
params = param.getParams(sys.argv[1])
params['type'] = sys.argv[1]
params['subtype'] = sys.argv[2]
tools = profiles.Toolkit()
makeFeed(params)	
