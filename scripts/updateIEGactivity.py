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
import logging
from datetime import datetime
import grantsbot_settings

wiki = wikitools.Wiki(grantsbot_settings.apiurl)
wiki.login(grantsbot_settings.username, grantsbot_settings.password)
conn = MySQLdb.connect(host = grantsbot_settings.host, db = grantsbot_settings.dbname, read_default_file = grantsbot_settings.defaultcnf, use_unicode=1, charset="utf8")
cursor = conn.cursor()
curtime = str(datetime.utcnow())

##FUNCTIONS##
def updateProfiles(cursor):
	"""
	Adds new profiles in, if there are any. Logs any new profiles.
	"""
	new_profiles = []
	cursor.execute('''
	insert ignore into ieg_profiles
		(rev_id, rev_user, rev_user_text, rev_timestamp, rev_comment, post_date)
		select rev_id, rev_user, rev_user_text, rev_timestamp, rev_comment, str_to_date(rev_timestamp, '%Y%m%d%H%i%s')
		from metawiki_p.revision
		where rev_page = 2101758
		and rev_comment like "/* {{subst:REVISIONUSER}} */ new section"
	''')
	conn.commit()
	cursor.execute('SELECT rev_user_text FROM ieg_profiles WHERE DATE(post_date) = DATE(NOW())')
	news = cursor.fetchall()
	if len(news) > 0:
		for new in news:
			new_profiles.append(new)
			logging.info('Added new profiles for ' + ' '.join(new_profiles) + ' at ' + curtime)
	else:
		logging.info('No new profiles added at ' + curtime)


def updatePagelist(cursor):
	"""
	Updates the list of pages under Grants:IdeaLab and Grants:IEG.
	If there are any. Calculates the number of recent edits to those
	pages by editors with profiles.
	"""
	cursor.execute('''
	insert ignore into ieg_pages (page_id, page_namespace, page_title, page_touched) select page_id, page_namespace, page_title, page_touched from metawiki_p.page where page_namespace in (200,201) and (page_title like "IdeaLab%" OR page_title LIKE "IEG%")
	''')
	conn.commit()
	cursor.execute('''
	UPDATE ieg_profiles AS h, (SELECT rev_user, COUNT(rev_id) AS recent_edits FROM metawiki_p.revision AS r, ieg_pages AS p WHERE r.rev_user IN (SELECT rev_user FROM ieg_profiles) AND r.rev_page = p.page_id AND r.rev_timestamp > DATE_FORMAT(DATE_SUB(NOW(),INTERVAL 30 DAY),"%Y%m%d%H%i%s") GROUP BY rev_user) AS tmp
	SET h.recent_edits = tmp.recent_edits WHERE h.rev_user = tmp.rev_user AND h.rev_user != 0
	''')
	conn.commit()

##MAIN##
updateProfiles(cursor)
updatePagelist(cursor)
cursor.close()
conn.close()
