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

import MySQLdb
import profiles
import grantsbot_settings
import output_settings
import sys

###FUNCTIONS###
def rankProfiles():
	"""
	rank Eval portal profiles by number of recent edits.
	"""
	profile_page = profiles.Profiles(params['output path'], params['output page id'], params)
	profile_list = profile_page.getPageSectionData(level = params['profile toclevel'])
# 	print profile_list
	for profile in profile_list:
		profile['title'].encode("utf8")#so redundant!
	quote1 = "'"
	quote2 = "'"
	usernames = quote1 + "','".join(x['title'] for x in profile_list) + quote2	
	conn = MySQLdb.connect(host = grantsbot_settings.host, db = grantsbot_settings.dbname, read_default_file = grantsbot_settings.defaultcnf, use_unicode=True, charset="utf8")
	cursor = conn.cursor()
	query = "SELECT rev_user_text, recent_edits FROM eval_profiles WHERE rev_user_text IN (%s);" % usernames	
# 	print query
# 	print type(query)
	cursor.execute(query)
	rows = cursor.fetchall()
	output = [{'edits' : row[1], 'username' : row[0].decode("utf8")} for row in rows]
# 	print output
	for profile in profile_list:
		for o in output:
			if profile['title'] == o['username']:
				profile['edits'] = o['edits']
				break
# 			continue
	for profile in profile_list:
		if "edits" not in profile:
			profile['edits'] = 0
		profile['text'] = profile_page.getPageText(profile['index'])
# 	print len(profile_list)			
	plist_sorted = sorted(profile_list, key=lambda item: item['edits'], reverse = True)
	plist_text = {'profiles' :'\n\n'.join([x['text'] for x in plist_sorted])} 
	formatted_profiles = profile_page.formatProfile(plist_text)
	edit_summ = params['edit summary'] % (params['type'],)
	profile_page.publishProfile(formatted_profiles, params['output path'], edit_summ, edit_sec = params['output section'])


###MAIN###
param = output_settings.Params()
params = param.getParams(sys.argv[1])
params['type'] = sys.argv[1]
rankProfiles()
