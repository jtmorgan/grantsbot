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
import logging
import categories
import profiles.py

wiki = wikitools.Wiki(grantsbot_settings.apiurl)
wiki.login(grantsbot_settings.username, grantsbot_settings.password)
conn = MySQLdb.connect(host = grantsbot_settings.host, db = grantsbot_settings.dbname, read_default_file = grantsbot_settings.defaultcnf, use_unicode=1, charset="utf8")
cursor = conn.cursor()


##GLOBAL VARIABLES##
curtime = str(datetime.utcnow())
page_namespace = "User_talk:"

# lists to track who needs a reminder
recipients = []


##GLOBAL VARIABLES##
curtime = str(datetime.utcnow())
page_namespace = 'User_talk:'

# lists to track who needs a reminder
recipients = []

# the reminder template
message_template = u'{{subst:Template:IEG/GrantsBot/Reminder|signature=~~~~}}'


##FUNCTIONS##
#gets a list of editor's to message
def getPages():
	category = categories.Categories("IEG_2013_round_2", 200) #namespace redundancy
	member_list = category.getCatMembers()
	print member_list

##FUNCTIONS##
#gets a list of editor's to message
def getUsernames(cursor):
	cursor.execute('SELECT pc_username FROM ieg_proposals WHERE p_status = "draft" AND p_creator_userid != 0 AND ieg_round_2 = 1')
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
		try:
			page.edit(message_template, section="new", sectiontitle="== Individual Engagement Grant proposals due 15 February 2013 ==", summary="Automatic reminder to complete a submitted [[Grants:IEG|Individual Engagement Grant Proposal]]", bot=1)
			try: #update the db to show that this user has been reminded
				cursor.execute('UPDATE ieg_proposals SET pc_reminded = 1 WHERE pc_username = "%s"' % (name,))
				conn.commit()
			except:
				logging.info('UPDATE: Could not update reminded status for User:' + name + ' at ' + curtime)
				continue
		except:
			logging.info('REMIND: Reminder to User:' + name + ' failed at to send at ' + curtime)
			continue


##MAIN##
rows = getUsernames(cursor)
if rows:
	for row in rows:
		name = row[0]
		recipients.append(name)
	messageUsers()
	logging.info('REMIND: Sent reminders to ' + ' '.join(recipients) + ' ' + curtime)
else:
	logging.info('REMIND: No reminders on ' + curtime)
cursor.close()
conn.close()






