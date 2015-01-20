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
import grantsbot_settings
import output_settings
import profiles
import sys

###FUNCTIONS###
def getGrantReports():
	category=categories.Categories('Reports_for_WMF_grants_funded_in_FY_2011-12')
	member_list = category.getCatMembers()
	return member_list

def getLearnings(grant_pages): #should this always be the same name
	for page in grant_pages:
		report = profiles.Profiles(page['page path'], page['page id'], settings = params)
		rep_secs = report.getPageSectionData()
		for sec in rep_secs:
			if sec['title'] == 'Lessons learned':
				page['lessons'] = report.getPageText(sec['index'])
				page['title'] = page['page path'][7:-7]
				page['formatted'] = report.formatProfile(page)			
# 				print page['lessons']
				continue
			else:
				pass
	grant_pages = [p for p in grant_pages if p.has_key("lessons")]		
	return grant_pages			
	
def publishLearnings(learning_pages):
	report = params['header template'] + '\n'.join(page['formatted'] for page in learning_pages)
# 	print report
	edit_sum = params['edit summary']
	pub = profiles.Profiles(params['output path'], params['type'])
	pub.publishProfile(report, params['output path'], edit_sum)		

###MAIN###
tools = profiles.Toolkit()
param = output_settings.Params()
params = param.getParams(sys.argv[1])
params['type'] = sys.argv[1]
grant_pages = getGrantReports()
learning_pages = getLearnings(grant_pages)
publishLearnings(learning_pages)