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
import output_parameters
import re
import shelve
import sys

logging.basicConfig(filename = grantsbot_settings.logs + 'makes.log', level = logging.INFO)
curtime = str(datetime.utcnow())

###FUNCTIONS###
def makeIdeaProfiles(profile_type, profile_subtype):
	"""
	create featured idea profiles and post them to a gallery.
	"""
	#do I need a 'params.py' file? What would go in it?
# 	profile_elements = {'summary' : '|summary'}
# 	profile_action_param = {'Category:IEG/Proposals/Participants' : '3', 'Category:IEG/Proposals/Draft/IdeaLab' : '4', 'Category:IEG/Proposals/IdeaLab' : '1'} #abstract this
	param = output_parameters.Params()
	params = param.getParams(profile_type)
	cat = params['category']
	category = categories.Categories(cat, 200) #namespace redundancy
	member_list = category.getCatMembers()
	member_list = member_list[0:4] #use sublist for quicker tests
# 	print member_list
# 	profiles_formattedx = [] #this is a crappy workaround. fix it.
# 	i = 6 #for featured ideas and featured people, different conditions should be assigned to different gallery pages.
	i = 0
	for member in member_list:
		if i < params['number featured']:
			member['datetime_added'] = dateutil.parser.parse(member['datetime_added']).strftime('%x') #assign cat added date
			profile = profiles.Profiles(member['page_path'], profile_type)
			touched = page.getPageInfo('touched')
	# 		print touched
	# 		started = dateutil.parser.parse(touched).strftime('%x')
			member['time'] = "Last edited: " + dateutil.parser.parse(touched).strftime('%x') #assign last edit date. do I need the middle variable-assignment step?
			member['action'] = params[profile_subtype]['action'] #assign action variable
			print action
	# 		for k, v in profile_action_param.iteritems():
	# 			if cat_title == k:
	# 				member['action'] = v
			infobox = profile.getPageText(0) #infoboxes are always in the top section
			text_val = params['summary']
			for line in infobox.split('\n'):
	# 			for k, v in profile_elements.iteritems():
	# 				if line.startswith(v, 0, len(v)):
	# 					try:
	# 						m = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
	# 						member[k] = m
	# 					except:
	# 						print "cannot find the template parameter " + k + " in " member['title']
				if line.startswith(text_val, 0, len(text_val)):
					try:
						txt = re.search('(?<=\=)(.*?)(?=<|$)',line).group(1)
						member['summary'] = txt
					except:
						print "cannot find the template parameter " + text_val + " in " member['title']
			member[profile_type] = re.search('([^/]+$)', member['page_path']).group(1) #am I still using page_path here?
			print member [profile_type]
			profile_formatted = profile.formatProfile(member)
			edit_summ = member['edit summary'] % profile_type
			path = params['output page']
			sub_page = params[profile_subtype]['first subpage']
			sub_page += i
			profile.publishProfile(profile_formatted, profile_type, edit_summ, sub_page)
	# 		print profile_formatted
			profiles_formattedx.append(profile_formatted)
			i += 1
		else:
			print "run complete"
# 	return profiles_formattedx
	profiles_textx = '\n\n'.join(x for x in profiles_formattedx)
	print profiles_textx

def	makePersonProfiles(profile_type, profile_subtype):
	"""
	create featured people profiles and publish them to a gallery
	"""
	param = output_parameters.Params()
	params = param.getParams(profile_type)
	profile_page = profiles.Profiles(params['main page'], profile_type)
	profile_list = profile_page.getPageSectionData()
	for profile in profile_list:
		profile['text'] = profile_page.getPageText(profile['profile_index'])
		main_edits = profile_page.getUserRecentEdits(profile['username'], 200)
		talk_edits = profile_page.getUserRecentEdits(profile['username'], 201)
		profile['edits'] = main_edits + talk_edits
	plist_sorted = sorted(profile_list, key=lambda item: item['edits'], reverse = True)
	plist_sorted = plist_sorted[0:4] #use sublist for quicker tests
	print plist_sorted

###MAIN###
profile_type = sys.argv[1] #you specify the kind of profile you want at the command line. Currently 'featured idea' or 'featured person'.
profile_subtype = sys.argv[2] #specify the subtype, e.g. 'new', 'draft', 'recent'
if profile_type == 'featured idea':
	makeIdeaProfiles(profile_type, profile_subtype)
elif profile_type == 'featured person':
	makePersonProfiles(profile_type, profile_subtype)
else:
	print "unrecognized profile type " + profile_type
logging.info('Made some ' + profile_type + 'profiles today, ' + curtime)