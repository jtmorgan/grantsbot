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
import dateutil.parser
from datetime import datetime, timedelta
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
	print member_list
	if profile_type == 'featured idea':
		makeFeaturedProfiles(profile_type, profile_subtype, params, category, member_list)
	elif profile_type == 'idea profile':
		makeProfileList(profile_type, profile_subtype, params, category, member_list)
	else:
		print 	"unrecognized idea profile type" #this shouldn't be necessary

def makeFeaturedProfiles(profile_type, profile_subtype, params, category, member_list):
	"""
	make featured profiles and post them each to a separate gallery page
	"""
	date_since = datetime.utcnow()-timedelta(days=120) #the date 30 days ago
	date_since = date_since.strftime('%Y%m%d%H%M%S')
# 	member_list = member_list[0:2] #use sublist for quicker tests
	i = 0
	for member in member_list:
		if i < params['number featured']:
			member['datetime added'] = dateutil.parser.parse(member['datetime added']).strftime('%x') #assign cat added date
			profile = profiles.Profiles(member['page path'], profile_type, id=member['page id'])
# 			touched = profile.getPageInfo('touched', 'info') #not sure I need this. date is not accurate
			latest = profile.getPageInfo('timestamp', 'revisions')
			print latest
			member['time'] = "Last edited: " + dateutil.parser.parse(latest).strftime('%x')
			member['action'] = params[profile_subtype]['action'] #assign action variable
			if profile_subtype == "participants":
				member['participants'] = profile.getPageRecentEditInfo(date_since)
			else:
				member['participants'] = ""
			infobox = profile.getPageText(0) #infoboxes are always in the top section
			sum_regex = params['summary']
			for line in infobox.split('\n'):
				if re.search(sum_regex, line):
					try:
						sum = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
						member['summary'] = sum.strip()
						member['summary'] = re.sub("(\[\[)(.*?)(\|)","",member['summary'])
						member['summary'] = re.sub("\]","",member['summary'])
						member['summary'] = re.sub("\[","",member['summary'])
						member['summary'] = (member['summary'][:140] + '...') if len(member['summary']) > 140 else member['summary'] #trims all summaries to 140 characters
					except:
						print "cannot find the template parameter " + sum_regex
			member['title'] = re.search('([^/]+$)', member['page path']).group(1)
			profile_formatted = profile.formatProfile(member)
			edit_summ = params['edit summary'] % profile_type
			path = params['output path'] #also need number of people, at some point
			sub_page = params[profile_subtype]['first subpage']
			sub_page += i
			profile.publishProfile(profile_formatted, path, edit_summ, sub_page)
			i += 1
		else:
			print "run complete"
			break

def makeProfileList(profile_type, profile_subtype, params, category, member_list):
	"""
	make basic idea profiles and post them as a list to a category-specific profile page
	"""
	date_since = datetime.utcnow()-timedelta(days=30) #the date 30 days ago
	date_since = date_since.strftime('%Y%m%d%H%M%S')
	if profile_subtype == 'new':
		member_list = member_list[0:10] #only the most recently added ideas
	else:
		pass
	plist = []
	for member in member_list:
		member['datetime added'] = dateutil.parser.parse(member['datetime added']).strftime('%x') #assign cat added date
		profile = profiles.Profiles(member['page path'], profile_type, member['page id'])
# 		touched = profile.getPageInfo('touched', 'info')
		latest = profile.getPageInfo('timestamp', 'revisions')
		member['time'] = "Last edited: " + dateutil.parser.parse(latest).strftime('%x')
		member['participants'] = profile.getPageRecentEditInfo(date_since)
		infobox = profile.getPageText(0) #infoboxes are always in the top section
		sum_regex = params['summary']
		creator_regex = params['creator']
		sum = ""
		cr = ""
		for line in infobox.split('\n'):
			if re.search(sum_regex, line):
				try:
					sum = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
					member['summary'] = sum
				except:
					print "could not get summary"
			else:
				pass
			if re.search(creator_regex, line):
				try:
					cr = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
				except:
					print "could not get creator"
			else:
				pass
		if len(cr) > 0:
			member['creator'] = cr
		else:
			member['creator'] = ""
# 		print member['creator']
		member['title'] = re.search('([^/]+$)', member['page path']).group(1)
		member['profile'] = profile.formatProfile(member)
	member_list.sort(key=operator.itemgetter('time'), reverse=True) #abstract this?
	ptext = '\n'.join(member['profile'] for member in member_list) #join 'em all together
	edit_summ = params['edit summary'] % (profile_subtype + " " + profile_type)
	path = params['output path']
	sub_page = params[profile_subtype]['subpage']
	profile.publishProfile(ptext, path, edit_summ, sub_page)



def	makePersonProfiles(profile_type, profile_subtype): #only for most active ones, for now
	"""
	create featured people profiles and publish them to a gallery
	"""
	param = output_params.Params()
	params = param.getParams(profile_type)
# 	print params['main page']
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
			member['time'] = "Last edited: " + dateutil.parser.parse(recent_edit).strftime('%x')
			member['action'] = params[profile_subtype]['action']
			member['page path'] = "User:" + member['username']
			sum = params['summary'] #crappy workaround
			img = params['image']
			bdg = params['badge']
			for line in member['text'].split('\n'):
				if line.startswith(bdg, 0, len(bdg)):
					try:
						txt = re.search('(?<=\=)(.*?)(?=<|\||$)',line).group(1)
						member['badge'] = txt.strip()
					except:
						print "cannot find the template parameter " + img
				if line.startswith(img, 0, len(img)):
					try:
						txt = re.search('(?<=\=)(.*?)(?=<|\||$)',line).group(1)
						member['image'] = txt.strip()
					except:
						print "cannot find the template parameter " + img
				if line.startswith(sum, 0, len(sum)):
					try:
						txt = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
						member['summary'] = txt.strip()
						member['summary'] = re.sub("(\[\[)(.*?)(\|)","",member['summary'])
						member['summary'] = re.sub("\]","",member['summary'])
						member['summary'] = re.sub("\[","",member['summary'])
						member['summary'] = (member['summary'][:140] + '...') if len(member['summary']) > 140 else member['summary'] #trims all summaries to 140 characters
					except:
						print "cannot find the template parameter " + sum
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
	all_member_list = []
	for profile_subtype in subtype_list:
# 		print profile_subtype
		cat = params[profile_subtype]['category']
		category = categories.Categories(cat, 200) #namespace redundancy
		member_list = category.getCatMembers()
		print member_list
		member_list.sort(key=operator.itemgetter('datetime added'), reverse=True) #abstract this?

		member_list = member_list[0:6] #only the 6 most recently added ideas
# 		print member_list

		for member in member_list:
			profile = profiles.Profiles(member['page path'], profile_type, member['page id'])
			member['title'] = re.search('([^/]+$)', member['page path']).group(1)
			member['time'] = dateutil.parser.parse(member['datetime added']).strftime('%x') #assign cat added date
			member['action'] = params[profile_subtype]['action'] #assign action variable
			infobox = profile.getPageText(0) #infoboxes are always in the top section
			creator_regex = params['creator']
			for line in infobox.split('\n'):
				if re.search(creator_regex, line):
					try:
						cr = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
						member['creator'] = cr.strip()
						break
					except:
						print "could not get creator"
				else:
					member['creator'] = ""
# 		print member_list
# 	print all_member_list
	all_member_list = [x for x in all_member_list if len(x.get('creator')) > 0]
	all_member_list.sort(key=operator.itemgetter('time'), reverse=True) #abstract this?
	seen = [] #we're removing stuff we've seen
	unique_member_list = []
	for member in all_member_list:
		t = member['page path']
		if t not in seen:
			seen.append(t)
			unique_member_list.append(member)
		else:
			print member['page path']
			pass
	print unique_member_list
	###including people###
	people_list = []
	date_since = datetime.utcnow()-timedelta(days=90) #the date 30 days ago
	date_since = date_since.strftime('%Y%m%d%H%M%S')
	profile = profiles.Profiles("Grants:IdeaLab/Introductions", profile_type, 2101758)
	people = "people"
	intro_list = profile.getPageRecentEditInfo(date_since, people)
	for intro in intro_list:
		intro['time'] = dateutil.parser.parse(intro['datetime added']).strftime('%x')
		intro['title'] = ""
		intro['page path'] = ""
		unique_member_list.append(intro)
	unique_member_list.sort(key=operator.itemgetter('time'), reverse=True) #abstract this?

# 	print seen
	print unique_member_list
	unique_member_list = unique_member_list[0:10] #only the most recently added ideas
# 	print all_member_list
	i = 1
	for member in unique_member_list:
		member['item'] = i
		i += 1
		member['profile'] = profile.formatProfile(member)
# 	print unique_member_list
	ptext = params['header template'] + '\n'.join(member['profile'] for member in unique_member_list) #join 'em all together
	edit_summ = params['edit summary'] % (profile_type)
	path = params['output path']
	profile.publishProfile(ptext, path, edit_summ)





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