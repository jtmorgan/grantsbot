#! /usr/bin/env python2.7

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
import grantsbot_settings
import logging
import output_params
import profiles #should really be using a different module here
import sys

logging.basicConfig(filename = grantsbot_settings.logs + 'proposals.log', level = logging.INFO)
curtime = str(datetime.utcnow())

##FUNCTIONS##
def checkCompleteness(p_type, subtype_list):
	"""
	Checks whether certain sections of a proposal have been completed.
	If so, removes a button template from the proposal page
	"""
	param = output_params.Params()
	params = param.getParams(p_type)
	tools = profiles.Toolkit()
	all_member_list = []
	for subtype in subtype_list:
		cat = params[subtype]['category']
		category = categories.Categories(cat, 200) #namespace redundancy
		member_list = category.getCatMembers()
		all_member_list.extend(member_list)
	all_member_list = all_member_list[0:6] #only the most recent proposals
	all_member_list = tools.dedupeMemberList(all_member_list, 'page path', 'page path')
# 	print all_member_list
	for member in all_member_list:
		p_page = profiles.Profiles(member['page path'], p_type, member['page id'])
		sec_list = p_page.getPageSectionData()
		for sec in sec_list:
			if sec['username'].startswith(params['button header']):
# 				print member['page path']
				edit_sec = int(sec['profile index']) - 1
				p_text = p_page.getPageText(edit_sec)
				if params['button template'] in p_text:
					p_text = p_text.replace(params['button template'], "")
					edit_summ = params['edit summary'] % (p_type)
					p_page.publishProfile(p_text, member['page path'], edit_summ, edit_sec = edit_sec)
					logging.info('Removed button from section ' + str(edit_sec) + " on proposal " + member['page path'] + " at " + curtime)
				else:
					pass
			else:
				pass

##MAIN##
p_type = sys.argv[1] #try "ieg proposal"
if p_type == 'ieg_proposal':
	subtype_list = ['draft','proposed','ineligible', 'withdrawn']
	checkCompleteness(p_type, subtype_list)
else:
	logging.info('Unrecognized proposal type ' + p_type + " " + curtime)

