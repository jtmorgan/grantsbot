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
import output_settings
import profiles
import re
import sys
import templates

###FUNCTIONS
def makeGallery():
	"""
	Makes featured profiles for Evalportal galleries.
	"""
	if params['subtype'] in ['learning_pattern', 'case_study', 'learning_module', 'intro', 'question']:
		featured_list = getFeaturedProfiles()
	else:
		sys.exit("unrecognized featured content type " + params['subtype'])	
	prepOutput(featured_list)				

def getFeaturedProfiles():
	"""
	Gets info about the top-billed profiles in a guide.
	"""
	featured_list = []
	profile_page = profiles.Profiles(params[params['subtype']]['input page path'], params[params['subtype']]['input page id'], params)
	profile_list = profile_page.getPageSectionData(level = params[params['subtype']]['profile toclevel'])
	for profile in profile_list:
		text = profile_page.getPageText(profile['index'])
		profile = profile_page.scrapeInfobox(profile, text)
		if params['subtype'] == 'intro':
			profile['page path'] = params[params['subtype']]['input page path'] + "#" + profile['title'].lstrip()
			if len(profile['name']) > 1: 
				profile['title'] = profile['name']
			else:
				pass			
			featured_list.append(profile)
		elif params['subtype'] == 'question':
			profile['summary'] = re.sub("\=\=(.*?)\=\=", "", text) #remove the question title from the summary.
			profile['page path'] = params[params['subtype']]['input page path'] + "#" + profile['title'].lstrip()
			featured_list.append(profile)
		else:
			if len(profile['summary']) > 1:
				featured_list.append(profile)
			else:
				pass
	for f in featured_list:
		f['action'] = params[params['subtype']]['action']
		f['summary'] = tools.formatSummaries(f['summary'])	
	return featured_list		
	
def prepOutput(featured_list):
	subpage = params[params['subtype']]['first subpage']
	i = 0
	number_featured = params[params['subtype']]['number featured']
	featured_list = tools.addDefaults(featured_list)       		
	output = profiles.Profiles(params[params['subtype']]['output path'], settings = params) #stupid tocreate a new profile object here. and stupid to re-specify the path below
	for f in featured_list:
		if i < number_featured:
			f['profile'] = output.formatProfile(f)
			f['profile'] = params['header template'] + '\n' + f['profile']
			edit_summ = params['edit summary'] % (params['subtype'] + " " + params['type'])
			output.publishProfile(f['profile'], params[params['subtype']]['output path'], edit_summ, sb_page = subpage)
			i += 1
			subpage += 1 #should fix idealab gallery to make this work there, too
		else:
			break	

###MAIN
param = output_settings.Params()
params = param.getParams(sys.argv[1])
params['type'] = sys.argv[1]
params['subtype'] = sys.argv[2]
tools = profiles.Toolkit()
makeGallery()	