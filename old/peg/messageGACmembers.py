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
import wikitools
import grantsbot_settings
from datetime import datetime
import templates

wiki = wikitools.Wiki(grantsbot_settings.apiurl)
wiki.login(grantsbot_settings.username, grantsbot_settings.password)
conn = MySQLdb.connect(host = grantsbot_settings.host, db = grantsbot_settings.dbname, read_default_file = grantsbot_settings.defaultcnf, use_unicode=1, charset="utf8")
cursor = conn.cursor()


##GLOBAL VARIABLES##
curtime = str(datetime.utcnow())
page_namespace = "User_talk:"

# lists to track who needs a reminder
recipients = []

# the reminder template
message_templates = templates.Template()
tmplt = message_templates.getTemplate('gac_reminder')

##FUNCTIONS##

def updateGACtivity(cursor):
	cursor.execute('update gac_members set active = 0;')#reset active status
	conn.commit()
	cursor.execute('UPDATE gac_members as h, (SELECT rev_user, COUNT(rev_id) AS recent_edits FROM metawiki_p.revision AS r, metawiki_p.page as p WHERE r.rev_user IN (SELECT user_id FROM gac_members) AND r.rev_page = p.page_id AND p.page_namespace = 201 and r.rev_timestamp > DATE_FORMAT(DATE_SUB(NOW(),INTERVAL 3 MONTH),"%s") GROUP BY r.rev_user) AS tmp SET h.recent_edits = IF(tmp.recent_edits, tmp.recent_edits, 0), h.active = IF(tmp.recent_edits, 1, 0) WHERE h.user_id = tmp.rev_user;' % ("%Y%m%d%H%i%s")) #sets everyone's status
	conn.commit()
	
#gets a list of editor's to message
def getUsernames(cursor):
	cursor.execute('SELECT user_name FROM gac_members WHERE active = 0 AND doNotMessage IS NULL;')
	rows = cursor.fetchall()
	if rows:
		return rows
	else:
		pass
		

#send the reminder message		
def messageUsers():
	for name in recipients:
		page_title = page_namespace + name
		page = wikitools.Page(wiki, page_title)
		page.edit(tmplt, section="new", summary="Automatic reminder to participate in [[Grants_Advisory_Committee|GAC]] activities", bot=1)


			
##MAIN##
#updateGACtivity(cursor)
rows = getUsernames(cursor)
if rows:
	for row in rows:
		name = row[0]
		recipients.append(name)
# 	print recipients			
	messageUsers()
cursor.close()
conn.close()






