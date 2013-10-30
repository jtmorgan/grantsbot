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
from datetime import datetime
import grantsbot_settings
from warnings import filterwarnings

conn = MySQLdb.connect(host = grantsbot_settings.host, db = grantsbot_settings.dbname, read_default_file = grantsbot_settings.defaultcnf, use_unicode=True, charset="utf8")
cursor = conn.cursor()
curtime = str(datetime.utcnow())
filterwarnings('ignore', category = MySQLdb.Warning)

##FUNCTIONS##
def updateProfiles(cursor):
	"""
	Adds new profiles in, if there are any. Logs any new profiles.
	"""
	cursor.execute('''
insert ignore into eval_profiles
		(rev_id, rev_user, rev_user_text, rev_timestamp, rev_comment, post_date, p_path, page_id)
		select rev_id, rev_user, rev_user_text, rev_timestamp, rev_comment, str_to_date(rev_timestamp, '%s'), page_title, page_id
		from metawiki_p.revision as r, metawiki_p.page as p
		where r.rev_page = 2344396 
		AND r.rev_page = p.page_id
		and rev_comment like "/* {{subst:REVISIONUSER}} */ new section"
	''' % ("%Y%m%d%H%i%s",))
	conn.commit()

#actually updates now!
	cursor.execute('''
UPDATE  eval_profiles a
        LEFT JOIN 
        (
            SELECT  rev_user_text, COUNT(*) RecentRevs 
            FROM    metawiki_p.revision
            WHERE   rev_timestamp > DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 14 DAY), '%s')
            AND rev_page IN (SELECT page_id FROM eval_pages UNION SELECT page_id FROM eval_patterns)
            GROUP   BY rev_user_text
        ) b ON a.rev_user_text = b.rev_user_text
SET     a.recent_edits = COALESCE(b.RecentRevs, 0);
	''' % ("%Y%m%d%H%i%s",))
	conn.commit()	

def updatePagelist(cursor):
	"""
	Updates the list of pages that are subpages of Programs:Evaluation portal OR that are in the right category.
	"""
	cursor.execute('''
	INSERT IGNORE INTO eval_pages (page_id, p_path, p_namespace, p_is_redirect, re_rev) SELECT page_id, page_title, page_namespace, page_is_redirect, page_latest FROM metawiki_p.page AS p WHERE p.page_title LIKE "Evaluation_portal%" AND p.page_namespace IN (208, 209);
	''')
	conn.commit()
	cursor.execute('''
	INSERT IGNORE INTO eval_pages (page_id, p_path, p_namespace, re_rev) 
SELECT 
	m.page_id,
	m.page_title,
	m.page_namespace,
	m.page_latest
FROM 
	metawiki_p.page AS m
	INNER JOIN 
	metawiki_p.categorylinks AS cl
ON 
	m.page_id = cl.cl_from 
WHERE 
	cl.cl_to IN ('Evaluation_portal') 
AND 
	cl.cl_type = 'page';
	''')
	conn.commit()

def updatePatternInfo(cursor):
	"""
	Adds in newly-created patterns, updates endorsements of patterns
	"""
	cursor.execute('''
	INSERT IGNORE INTO eval_patterns (page_id, p_path, p_namespace, re_rev) 
SELECT 
	m.page_id,
	m.page_title,
	m.page_namespace,
	m.page_latest
FROM 
	metawiki_p.page AS m
	INNER JOIN 
	metawiki_p.categorylinks AS cl
ON 
	m.page_id = cl.cl_from 
WHERE 
	cl.cl_to IN ('Learning_patterns') 
AND 
	cl.cl_type = 'page';
	''')
	conn.commit()
	#number of endorsements
	cursor.execute('''
	UPDATE eval_patterns AS lp, (SELECT COUNT(rev_comment) as endorse, rev_page FROM metawiki_p.revision AS r WHERE r.rev_page IN (SELECT page_id FROM eval_patterns) AND r.rev_comment LIKE "endorse%" GROUP BY rev_page) AS tmp SET lp.endorsements = 
CASE
	WHEN tmp.endorse = 0 THEN 0
	ELSE tmp.endorse
END
WHERE lp.page_id = tmp.rev_page;
	''')
	conn.commit()
	#first edit to pattern
	cursor.execute('''
	UPDATE eval_patterns AS lp, (SELECT MIN(rev_timestamp) as time, rev_page, rev_id, rev_user, user_name FROM metawiki_p.revision AS r, metawiki_p.user AS u WHERE r.rev_page IN (SELECT page_id FROM eval_patterns) AND r.rev_user = u.user_id GROUP BY rev_page) AS tmp SET lp.pc_date = tmp.time, lp.pc_rev = tmp.rev_id, lp.p_creator = tmp.rev_user, lp.pc_username = tmp.user_name WHERE lp.page_id = tmp.rev_page;	
	''')
	conn.commit()
	#add recent edit metadata	
	cursor.execute('''
UPDATE eval_patterns AS ep, (SELECT page_title, MAX(max) as maxmax FROM 
	(SELECT page_title, page_id, rev_user, rev_user_text, page_namespace, MAX(rev_id) as max FROM metawiki_p.revision AS r, metawiki_p.page AS p WHERE r.rev_page = p.page_id AND p.page_namespace = 201 AND p.page_title IN (SELECT p_path FROM eval_patterns) GROUP BY page_id
		UNION 
	SELECT page_title, page_id, rev_user, rev_user_text, page_namespace, MAX(rev_id) as max FROM metawiki_p.revision AS r, metawiki_p.page AS p WHERE r.rev_page = p.page_id AND p.page_namespace = 200 AND p.page_title IN (SELECT p_path FROM eval_patterns) GROUP BY page_id) as tmp GROUP BY page_title) AS tmp2 
	SET ep.re_rev = tmp2.maxmax WHERE ep.p_path = tmp2.page_title; 
	''')
	conn.commit()
	cursor.execute('''
	UPDATE eval_patterns AS ep, metawiki_p.revision AS r SET ep.recent_editor = r.rev_user, ep.re_username = r.rev_user_text, ep.re_date = r.rev_timestamp WHERE r.rev_id = ep.re_rev;
	''')
	conn.commit()	#would be nice if I could customize this to "x commented on..."
	#add endorsers
	cursor.execute('''
	INSERT IGNORE INTO eval_pattern_endorsements (rev_id, rev_user, rev_user_text, rev_timestamp, rev_comment, page_id, p_path) SELECT rev_id, rev_user, rev_user_text, rev_timestamp, rev_comment, page_id, p_path FROM eval_patterns as ep, metawiki_p.revision AS r WHERE r.rev_comment LIKE "endorse%" AND r.rev_page = ep.page_id;
	''')
	conn.commit()
	
def updateQuestionInfo(cursor):
	"""		
	Add recent question info.
	"""
	cursor.execute('''
	INSERT IGNORE INTO eval_questions (rev_id, rev_user, rev_user_text, rev_timestamp, rev_comment, p_path, page_id) SELECT rev_id, rev_user, rev_user_text, rev_timestamp, rev_comment, page_title, rev_page FROM metawiki_p.revision AS r, metawiki_p.page AS p WHERE r.rev_page = 2344395 AND p.page_id = r.rev_page AND r.rev_comment LIKE "%new section";
	''')
	conn.commit()
	
##MAIN##
updateProfiles(cursor)
updatePagelist(cursor)
updatePatternInfo(cursor)
updateQuestionInfo(cursor)
cursor.close()
conn.close()
