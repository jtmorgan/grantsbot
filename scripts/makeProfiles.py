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
import profiles
import output_params
import re
import shelve
import sys
import templates
import operator

logging.basicConfig(filename = grantsbot_settings.logs + 'makes.log', level = logging.INFO)
curtime = str(datetime.utcnow())

###FUNCTIONS###
def makeIdeaProfiles(profile_type, profile_subtype):
	"""
	make profiles for IdeaLab ideas or IEG proposals
	"""
	param = output_params.Params()
	params = param.getParams(profile_type)
	cat = params[profile_subtype]['category']
	category = categories.Categories(cat, 200) #namespace redundancy
	member_list = category.getCatMembers()
	if profile_type == 'featured idea':
		makeFeaturedProfiles(profile_type, profile_subtype, params, category, member_list)
	elif profile_type == 'idea profile':
		makeProfileList(profile_type, profile_subtype, params, category, member_list)
	else:
		print 	"unrecognized idea profile type" #this shouldn't be necessary

def makeFeaturedProfiles(profile_type, profile_subtype, params, category, member_list):
	"""
	Make featured profiles and post them each to a separate gallery page.
	"""
	tools = profiles.Toolkit()
	date_since = tools.getSubDate(120)
# 	member_list = member_list[0:2] #use sublist for quicker tests
	i = 0
	for member in member_list:
		if i < params['number featured']: #this is problematic	
			profile = profiles.Profiles(member['page path'], profile_type, id=member['page id'])	
			member['participants'] = profile.getPageRecentEditInfo(date_since)
			if member['participants'] < 1:
				member['participants'] = ""
			else:
				pass
			member['datetime added'] = tools.parseISOtime(member['datetime added'])
			latest = profile.getPageInfo('timestamp', 'revisions')
			member['time'] = tools.parseISOtime(latest)
			member['action'] = params[profile_subtype]['action']
			infobox = profile.getPageText(0)
			sum_re = params['summary']
			for line in infobox.split('\n'):
				if re.search(sum_re, line):
					try:
						sum = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
						if len(sum) > 1:
							member['summary'] = tools.formatSummaries(sum)
						else:
							member['summary'] = ""	
					except:
						print "cannot find the template parameter " + sum_re
				else:
					member['summary'] = ""							
			member['title'] = re.search('([^/]+$)', member['page path']).group(1)
			member['profile'] = profile.formatProfile(member)
			sub_page = params[profile_subtype]['first subpage']
			sub_page += i
			profile.publishProfile(member['profile'], params['output path'], params['edit summary'] % profile_type, sub_page)
			i += 1
		else:
			break

def makeProfileList(profile_type, profile_subtype, params, category, member_list):
	"""
	Make basic idea profiles and post them as a list to a category-specific profile page.
	"""
	tools = profiles.Toolkit()
	date_since = tools.getSubDate(120)
	if profile_subtype == 'new':
		member_list = member_list[0:10] #only the most recently added ideas
	else:
		pass
	for member in member_list:
		member['datetime added'] = tools.parseISOtime(member['datetime added'])
		profile = profiles.Profiles(member['page path'], profile_type, member['page id'])
		latest = profile.getPageInfo('timestamp', 'revisions')
		member['time'] = tools.parseISOtime(latest)
		member['participants'] = profile.getPageRecentEditInfo(date_since)
		infobox = profile.getPageText(0)
		sum_re = params['summary']
		creator_re = params['creator']
		member['summary'] = ""
		member['creator'] = ""
		for line in infobox.split('\n'):
			if re.search(sum_re, line):
				try:
					member['summary'] = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
				except:
					print "could not get summary"
			else:
				pass
			if re.search(creator_re, line):
				try:
					member['creator'] = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
				except:
					print "could not get creator"
			else:
				pass
		member['title'] = re.search('([^/]+$)', member['page path']).group(1)
		member['profile'] = profile.formatProfile(member)
	member_list.sort(key=operator.itemgetter('time'), reverse=True) #abstract this?
	all_profiles = '\n'.join(member['profile'] for member in member_list)
	edit_summ = params['edit summary'] % (profile_subtype + " " + profile_type)
	sub_page = params[profile_subtype]['subpage']
	profile.publishProfile(all_profiles, params['output path'], edit_summ, sub_page)

def	makePersonProfiles(profile_type, profile_subtype): #only for most active ones, for now
	"""
	create featured people profiles and publish them to a gallery
	"""
	param = output_params.Params()
	params = param.getParams(profile_type)
	tools = profiles.Toolkit()	
	profile_page = profiles.Profiles(params['main page'], profile_type, id=2101758) #should the page id be baked in like this?
	profile_list = profile_page.getPageSectionData()
	profile_list = profile_list[0:6] #only need top six. assumes profiles are already sorted by activity
	i = 0
	for member in profile_list:
		if i < params['number featured']:
			member['text'] = profile_page.getPageText(member['profile index'])
			main_edits = profile_page.getUserRecentEditInfo(member['username'], 200)
			talk_edits = profile_page.getUserRecentEditInfo(member['username'], 201)
			member['edits'] = main_edits[0] + talk_edits[0]
			if main_edits[1] > talk_edits[1]:
				recent_edit = main_edits[2]
			else:
				recent_edit = talk_edits[2]
			member['time'] = dateutil.parser.parse(recent_edit).strftime('%x')
			member['action'] = params[profile_subtype]['action']
			member['page path'] = "User:" + member['username']
# 			sum_re = params['summary']
# 			img = params['image']
# 			bdg = params['bdg']
			for line in member['text'].split('\n'):
				if re.search(params['image'], line):
					try:
						img = re.search('(?<=\=)(.*?)(?=<|\||$)',line).group(1)
						if len(img) > 1:
							member['image'] = tools.formatSummaries(img)
						else:
							member['image'] = ""							
					except:
						print "cannot find the template parameter " + params['image']
				if re.search(params['badge'], line):
					try:
						bdg = re.search('(?<=\=)(.*?)(?=<|\||$)',line).group(1)
						if len(bdg) > 1:
							member['badge'] = tools.formatSummaries(bdg)
						else:
							member['badge'] = ""
					except:
						print "cannot find the template parameter " + params['badge']
				if re.search(params['summary'], line):
					try:
						sum = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
						if len(sum) > 1:
							member['summary'] = tools.formatSummaries(sum)
						else:
							member['summary'] = ""							
					except:
						print "cannot find the template parameter " + params['summary']
			profile = profiles.Profiles(member['page path'], profile_type) #fix this! inconsistent
			profile_formatted = profile.formatProfile(member)
			edit_summ = params['edit summary'] % profile_type
			path = params['output path']
			sub_page = params[profile_subtype]['first subpage']
			sub_page += i
			profile.publishProfile(profile_formatted, path, edit_summ, sub_page)
			i += 1

def makeActivityFeed(profile_type, subtype_list):
	"""
	make an activity feed with the most recent ideas in it
	"""
	param = output_params.Params()
	params = param.getParams(profile_type)
	tools = profiles.Toolkit()
	date_since = tools.getSubDate(90)
	all_member_list = []
	for subtype in subtype_list:
		cat = params[subtype]['category']
		category = categories.Categories(cat, 200) #namespace redundancy
		member_list = category.getCatMembers()
		member_list = member_list[0:6] #only the 6 most recently added ideas, for simplicity
		for member in member_list:
			member['subtype'] = subtype	
			member['action'] = params[member['subtype']]['action'] #put this in cat class	
		all_member_list.extend(member_list)
	for member in all_member_list:
		profile = profiles.Profiles(member['page path'], profile_type, member['page id'])
		member['title'] = re.search('([^/]+$)', member['page path']).group(1)
		member['time'] = tools.parseISOtime(member['datetime added']) #should put this in cat class
		member['participants'] = profile.getPageRecentEditInfo(date_since)
		if member['participants'] > 2:
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
						print "could not get creator"
				else:
					pass
	all_member_list = [x for x in all_member_list if len(x.get('creator')) > 0 or x.get('action') == 2] #only keep ones with a creator or more than two participants
	all_member_list = tools.dedupeMemberList(all_member_list, 'time', 'page path') #remove dupes
	all_member_list = addPeople(all_member_list, tools) #add recent people profiles
	all_member_list.sort(key=operator.itemgetter('time'), reverse=True) #abstract this?
	all_member_list = all_member_list[0:10] #only the most recently events
	i = 1
	for member in all_member_list:
		member['item'] = i
		i += 1
		member['profile'] = profile.formatProfile(member)
	all_profiles = params['header template'] + "".join(member['profile'] for member in all_member_list)
	edit_summ = params['edit summary'] % (profile_type)
	profile.publishProfile(all_profiles, params['output path'], edit_summ)

def addPeople(mem_list, tools):
	"""
	Add profiles of IdeaLab participants to the activity feed member list.
	"""
	date_since = tools.getSubDate(120)
	profile = profiles.Profiles("Grants:IdeaLab/Introductions", profile_type, 2101758) #needs abstraction
	people = "people" #boo!
	people_list = profile.getPageRecentEditInfo(date_since, people)
	for person in people_list:
		person['creator'] = "[[User:" + person['creator'] + "|" + person['creator'] + "]]"
		person['time'] = tools.parseISOtime(person['datetime added'])
		person['title'] = ""
		person['page path'] = ""
		person['participants'] = ""
	mem_list.extend(people_list)
	return mem_list


###MAIN###
profile_type = sys.argv[1] #you specify the kind of profile you want at the command line. Currently 'featured idea' or 'featured person'.
profile_subtype = sys.argv[2] #specify the subtype, e.g. 'new', 'draft', 'recent'

if ( profile_type == 'featured idea' or profile_type == 'idea profile' ):
	makeIdeaProfiles(profile_type, profile_subtype)
elif profile_type == 'featured person':
	makePersonProfiles(profile_type, profile_subtype)
elif profile_type == 'activity feed':
	subtype_list = ['new','draft','participants'] #we want to get all of these
	makeActivityFeed(profile_type, subtype_list)
else:
	print "unrecognized profile type " + profile_type
logging.info('Made some ' + profile_type + 'profiles today, ' + curtime)