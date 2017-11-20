#! /usr/bin/python2.7

# Copyright 2015 Jtmorgan

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
import grantsbot_settings
import wikitools

report_title = grantsbot_settings.rootpage + 'IdeaLab/Inspire/Leaderboard'

report_template = u'''==Endorsed ideas==
<!-- PLEASE DO NOT MAKE MANUAL CHANGES TO THIS SECTION OF THE PAGE. They will be overwritten next time the bot runs -->
This list is updated hourly. It  was last updated on {{subst:REVISIONMONTH}}/{{subst:REVISIONDAY}}/{{subst:REVISIONYEAR}} by [[User:{{subst:REVISIONUSER}}]]. Manual changes to this list will be overwritten the next time the bot runs.

{| class="wikitable sortable"
| align="center" style="background:#f0f0f0; font-weight:bold;"|idea
| align="center" style="background:#f0f0f0; font-weight:bold;"|endorsements
|-
%s
|}

</div><!-- END LEFT COLUMN -->

<!-- RIGHT COLUMN -->
<div style="float: {{dir|{{pagelang}}|left|right}}; width: %s; {{IdeaLab/Font}};">
<div style="font-size: 1.2em; padding-bottom: .5em;">Campaign progress</div>
{{Grants:IdeaLab/Inspire/Scoreboard}}
{{IdeaLab/Inspire/Feed}}
</div><!-- END RIGHT COLUMN -->

</div><!-- END WHOLE PAGE WRAPPER -->

[[Category:IdeaLab]]
[[Category:Inspire campaign]]
<!-- PLEASE ADD ADDITIONAL CATEGORIES TO THE TOP OF THE PAGE. Categories added to this section will be overwritten next time the bot runs -->
'''

##FUNCTIONS##
def get_ideas(cursor):
    """
    Get all Inspire ideas and their number of endorsements
    """
    table_data = []
    cursor.execute('''SELECT SUBSTRING_INDEX(page_title, "/", -1) AS idea_title, COUNT(rev_comment) as endorsements
FROM metawiki_p.page AS p 
JOIN metawiki_p.categorylinks AS cl 
ON p.page_id = cl.cl_from 
JOIN metawiki_p.revision AS r
ON p.page_id = r.rev_page
WHERE cl.cl_to ="IdeaLab/Ideas/Inspire/New_readers"
AND cl.cl_type = "page"
AND p.page_namespace = 200
AND p.page_title LIKE "IdeaLab/%"
AND p.page_title NOT LIKE "%/%/%"
AND p.page_id != 5322427
AND (r.rev_comment LIKE ("%Endorse%") OR r.rev_comment LIKE ("%endorse%")) GROUP BY idea_title ORDER BY endorsements DESC;''')
    rows = cursor.fetchall()
    for row in rows:
    	path = unicode(row[0],"utf-8")
    	title = path.replace("_"," ")
    	endorsements = row[1]
    	
    	endorsements = row[1]
        table_row = '''|[[Grants:IdeaLab/%s|%s]]
| %d
|-''' % (path, title, endorsements)   
    	table_data.append(table_row)	
    return table_data


##MAIN##
wiki = wikitools.Wiki(grantsbot_settings.apiurl)
wiki.login(grantsbot_settings.username, grantsbot_settings.password)
conn = MySQLdb.connect(host = grantsbot_settings.host, db = grantsbot_settings.dbname, read_default_file = grantsbot_settings.defaultcnf, use_unicode=True, charset="utf8")
cursor = conn.cursor()
table_data = get_ideas(cursor)
report = wikitools.Page(wiki, report_title)
report_text = report_template % ('\n'.join(table_data), "30%")
report_text = report_text.encode('utf-8')
# print report_text
report.edit(report_text, section=1, summary="automatic update of endorsements leaderboard", bot=1)
cursor.close()
conn.close()
