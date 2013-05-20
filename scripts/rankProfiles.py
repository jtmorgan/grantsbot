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

# from datetime import datetime
# import MySQLdb
import logging
import profiles
import grantsbot_settings
import wikitools

wiki = wikitools.Wiki(settings.apiurl)
wiki.login(settings.username, settings.password)
logging.basicConfig(filename= grantsbot_settings.logs + 'moves.log', level=logging.INFO)
# conn = MySQLdb.connect(host = grantsbot_settings.host, db = grantsbot_settings.db, read_default_file = '~/.my.cnf', use_unicode=1, charset="utf8" )
# curtime = str(datetime.utcnow())
# cursor = conn.cursor()
# page_namespace = (settings.rootpage)
page_title = "IdeaLab/Introductions"


### FUNCTIONS ###


def findProfiles(profile_page, contributors):
	profile_page = profiles.Profiles(page_title)
	profile_list = profile_page.getPageSectionData()
	for profile in profile_list:
		profile['text'] = profile_page.getPageSectionData(profile['profile_index'])
		main_edits = profile_page.getUserRecentEdits(profile['username'], 200)
		talk_edits = profile_page.getUserRecentEdits(profile['username'], 201)
		profile['edits'] = main_edits + talk_edits
	return profile_list

#returns the host profiles to the page, with the newest hosts on top
def returnProfiles(profile_page, profile_list):
	report_title = page_namespace + page_title
	report = wikitools.Page(wiki, report_title)
	template = open('/home/jtmorgan/grantsbot/scripts/profile_page_template.txt')
	report_template = template.read()
	profiles = report_template % '\n'.join([x[1] for x in profile_list])
	print profiles
# 	profiles = profiles.encode('utf-8')
# 	report.edit(profiles, section=0, summary="Reordering the host profiles, with newly-joined and highly-active hosts at the top", bot=1)

##main##
profile_list = findProfiles(profile_page, contributors)
print profile_list
# returnProfiles(profile_page, profile_list)

