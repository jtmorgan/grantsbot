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
from datetime import datetime
import grantsbot_settings
import logging
import profiles
import output_params
import re
import shelve
import sys
import templates

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
	make featured profiles and post them each to a separate gallery page
	"""
	member_list = member_list[0:2] #use sublist for quicker tests
	i = 0
	for member in member_list:
		if i < params['number featured']:
			member['datetime added'] = dateutil.parser.parse(member['datetime added']).strftime('%x') #assign cat added date
			profile = profiles.Profiles(member['page path'], member['page id'], profile_type)
			touched = profile.getPageInfo('touched')
			member['time'] = "Last edited: " + dateutil.parser.parse(touched).strftime('%x')
			member['action'] = params[profile_subtype]['action'] #assign action variable
			infobox = profile.getPageText(0) #infoboxes are always in the top section
			sum_regex = params['summary']
			for line in infobox.split('\n'):
				if re.search(sum_regex, line):
					try:
						sum = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
						member['summary'] = sum
					except:
						print "cannot find the template parameter " + sum_regex
			member['summary'] = (member['summary'][:140] + '...') if len(member['summary']) > 140 else member['summary'] #trims all summaries to 140 characters
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

def makeProfileList(profile_type, profile_subtype, params, category, member_list):
	"""
	make basic idea profiles and post them as a list to a category-specific profile page
	"""
	member_list = member_list[0:10] #only the most recently added ideas
	plist = []
	for member in member_list:
		member['datetime added'] = dateutil.parser.parse(member['datetime added']).strftime('%x') #assign cat added date
		profile = profiles.Profiles(member['page path'], member['page id'], profile_type)
		touched = profile.getPageInfo('touched')
		member['time'] = "Last edited: " + dateutil.parser.parse(touched).strftime('%x')
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
		plist.append(member['profile'])
	plist_text = '\n'.join(x for x in plist) #join 'em all together
# 	print plist_text
	edit_summ = params['edit summary'] % (profile_subtype + " " + profile_type)
	path = params['output path']
	sub_page = params[profile_subtype]['subpage']
	profile.publishProfile(plist_text, path, edit_summ, sub_page)



def	makePersonProfiles(profile_type, profile_subtype): #only for most active ones, for now
	"""
	create featured people profiles and publish them to a gallery
	"""
	param = output_params.Params()
	params = param.getParams(profile_type)
# 	print params['main page']
	profile_page = profiles.Profiles(params['main page'], profile_type)
	profile_list = profile_page.getPageSectionData()
	for member in profile_list:
			member['text'] = profile_page.getPageText(member['profile_index'])
			main_edits = profile_page.getUserRecentEditInfo(member['username'], 200)
			talk_edits = profile_page.getUserRecentEditInfo(member['username'], 201)
			member['edits'] = main_edits[0] + talk_edits[0]
			if main_edits[1] > talk_edits[1]:
				recent_edit = main_edits[2]
			else:
				recent_edit = talk_edits[2]
			member['time'] = "Last edited: " + dateutil.parser.parse(recent_edit).strftime('%x')
			member['action'] = params[profile_subtype]['action']
			sum = params['summary'] #crappy workaround
			ttle = params['page path']
			img = params['image']
			for line in member['text'].split('\n'):
				if line.startswith(ttle, 0, len(ttle)):
					try:
						txt = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
						member['page_path'] = txt.strip() #fix this! inconsistent
						member['featured idea'] = txt.strip()[5:]
					except:
						print "cannot find the template parameter " + ttle
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
					except:
						print "cannot find the template parameter " + sum
	plist_sorted = sorted(profile_list, key=lambda item: item['edits'], reverse = True)
	plist_sorted = plist_sorted[0:6] #use sublist for quicker tests
	i = 0
	for member in plist_sorted:
		if i < params['number featured']:
			profile = profiles.Profiles(member['page_path'], profile_type) #fix this! inconsistent
			profile_formatted = profile.formatProfile(member)
			edit_summ = params['edit summary'] % profile_type
			path = params['output path']
			sub_page = params[profile_subtype]['first subpage']
			sub_page += i
			profile.publishProfile(profile_formatted, path, edit_summ, sub_page)
			i += 1

# 	i = 0
# 		if i < params['number featured']:


###MAIN###
profile_type = sys.argv[1] #you specify the kind of profile you want at the command line. Currently 'featured idea' or 'featured person'.
profile_subtype = sys.argv[2] #specify the subtype, e.g. 'new', 'draft', 'recent'

if ( profile_type == 'featured idea' or profile_type == 'idea profile' ):
	makeIdeaProfiles(profile_type, profile_subtype)
elif profile_type == 'featured person':
	makePersonProfiles(profile_type, profile_subtype)
else:
	print "unrecognized profile type " + profile_type
logging.info('Made some ' + profile_type + 'profiles today, ' + curtime)