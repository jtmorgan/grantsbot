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

import csv
from datetime import datetime
import grantsbot_settings
import logging
import MySQLdb
# import pageData as p
import sys
import wikitools

# conn = MySQLdb.connect(host = 'metawiki-p.userdb.toolserver.org', db = 'u_jtmorgan_p', read_default_file = '~/.my.cnf', use_unicode=1, charset="utf8" )
# cursor = conn.cursor()
curtime = str(datetime.utcnow())
# logging.basicConfig(filename='/home/jtmorgan/grantsbot/logs/proposals.log',level=logging.INFO)
page_namespace = 'Grants:'

wiki = wikitools.Wiki(grantsbot_settings.apiurl)
wiki.login(grantsbot_settings.username, grantsbot_settings.password)
conn = MySQLdb.connect(host = grantsbot_settings.host, db = grantsbot_settings.dbname, read_default_file = grantsbot_settings.defaultcnf, use_unicode=1, charset="utf8")
cursor = conn.cursor()

##FUNCTIONS##
def updateActivity():
	"""
	Adds in new proposals, updates status of existing ones.
	"""
	#first, updates proposal activity table with new revs
	cursor.execute('''
INSERT IGNORE INTO ieg_proposal_edits (rev_id, rev_user, rev_user_text, rev_timestamp, rev_comment, page_id, page_title, page_namespace) SELECT rev_id, rev_user, rev_user_text, rev_timestamp, rev_comment, page_id, page_title, page_namespace FROM metawiki_p.page as p, metawiki_p.revision as r WHERE p.page_namespace IN (200, 201) AND p.page_title LIKE '%s' AND p.page_title NOT LIKE '%s' AND p.page_id = r.rev_page
	''' % ("IdeaLab/%", "IdeaLab/%/%"))
	conn.commit()
	rowsaffected = cursor.rowcount
	if rowsaffected > 0:
		#then, update proposal table with new proposals
		cursor.execute('''
INSERT IGNORE INTO ieg_proposals (page_id, page_title, p_created_date, p_latest_edit_date, p_creator_userid, pc_username) SELECT page_id, page_title, STR_TO_DATE(min, "%s"), STR_TO_DATE(max, "%s"), rev_user, rev_user_text FROM (SELECT MIN(rev_timestamp) as min, MAX(rev_timestamp) AS max, page_id, page_title, rev_timestamp, rev_user, rev_user_text FROM ieg_proposal_edits WHERE page_namespace = 200 GROUP BY page_id) AS tmp
		''' % ("%Y%m%d%H%i%s", "%Y%m%d%H%i%s"))
		conn.commit()


def updateStatus():
	"""
	Updates the status of the existing proposals by checking how they are categorized.
	"""
	#updates status of proposals through categorylinks
	cursor.execute('''UPDATE ieg_proposals AS p, (SELECT cl_from, cl_to FROM metawiki_p.categorylinks AS c, ieg_proposals AS pp WHERE c.cl_from = pp.page_id AND c.cl_to IN ("IEG/Proposals/Draft", "IEG/Proposals/Proposed", "IEG/Proposals/Ineligible", "IEG/Proposals/Withdrawn")) AS tmp
	SET p.p_status = CASE tmp.cl_to
	WHEN "IEG/Proposals/Draft" THEN 'draft'
	WHEN "IEG/Proposals/Proposed" THEN 'proposed'
	WHEN "IEG/Proposals/Ineligible" THEN 'ineligible'
	WHEN "IEG/Proposals/Withdrawn" THEN 'withdrawn'
	ELSE "not proposal"
	END
	WHERE tmp.cl_from = p.page_id''')
	conn.commit()
	#removes things that have once been categorized as active proposals, but have had those categories completely removed, from consideration
	cursor.execute('''UPDATE ieg_proposals SET p_status = 'category removed' WHERE p_status IN ("ineligible", "withdrawn", "draft", "proposed") AND page_id NOT IN (SELECT cl_from FROM metawiki_p.categorylinks WHERE cl_to IN ("IEG/Proposals/Draft", "IEG/Proposals/Proposed", "IEG/Proposals/Ineligible", "IEG/Proposals/Withdrawn"))''')
	conn.commit()

	cursor.execute('''UPDATE ieg_proposals AS p, (SELECT cl_from, cl_to FROM metawiki_p.categorylinks AS c, ieg_proposals AS pp WHERE c.cl_from = pp.page_id AND c.cl_to = "IEG_2013_round_2") AS tmp SET p.ieg_round_2 = 1 WHERE tmp.cl_from = p.page_id;''')
	conn.commit()


def updateDB(): #need to reconcile this with the similar function above
	"""
	Updates the under_review and in_idealab status of proposals.
	"""
	cursor.execute('''UPDATE ieg_proposals AS p, (SELECT cl_from, cl_to FROM metawiki_p.categorylinks AS c, ieg_proposals AS pp WHERE c.cl_from = pp.page_id AND c.cl_to IN ("IEG/Proposals/IdeaLab", "IEG/Proposals/Review") ORDER BY cl_from ASC) AS tmp
	SET p.p_in_idealab = CASE tmp.cl_to
	WHEN "IEG/Proposals/IdeaLab" THEN 1
	ELSE 0
	END,
	p.p_under_review = CASE tmp.cl_to
	WHEN "IEG/Proposals/Review" THEN 1
	ELSE 0
	END
	WHERE tmp.cl_from = p.page_id''')
	conn.commit()


def writeReport():
	"""
	Creates an output csv file.
	"""
	f = open(sys.argv[1], 'wt')
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow( ('ID','Proposal page', 'current status', 'under review (y/n)', 'in idealab (y/n)', 'Date created', 'Last edited', 'Submitter') )
	cursor.execute('SELECT id, page_title, p_status, p_under_review, p_in_idealab, p_created_date, p_latest_edit_date, pc_username FROM ieg_proposals WHERE ((p_status IS NOT NULL AND p_status != "not proposal") OR (p_under_review = 1 OR p_in_idealab = 1)) ORDER BY id ASC')
	rows = cursor.fetchall()
	for row in rows:
		data = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
		#writes a new line of data to output csv
		try:
			writer.writerow( (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]) )
		except ValueError:
			writer.writerow( ("error!") )



##MAIN##
updateActivity()
updateStatus()
# proposals = checkCompleteness()
updateDB()
# writeReport()
cursor.close()
conn.close()
