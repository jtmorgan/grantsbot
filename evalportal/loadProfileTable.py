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

import profiles
import grantsbot_settings
import MySQLdb

conn = MySQLdb.connect(host = grantsbot_settings.host, db = grantsbot_settings.dbname, read_default_file = grantsbot_settings.defaultcnf, use_unicode=1, charset="utf8")
cursor = conn.cursor()	

def findProfiles(cursor):
	profile_page = profiles.Profiles("Programs:Evaluation_portal/Parlor/Introductions", "whocares")
	profile_list = profile_page.getPageSectionData()
#	usernames = [x['username'] for x in profile_list]
	quote1 = "('"
	quote2 = "')"
	usernames = quote1 + "'),('".join(x['username'] for x in profile_list) + quote2
	print usernames
#for profile in profile_list:	
	cursor.execute("INSERT INTO eval_profiles (rev_user_text) VALUES%s;" % usernames)
	conn.commit()

findProfiles(cursor)
