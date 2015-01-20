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

class Query:
	"""
	 Bunch of queries used by GrantsBot to manage various portals.
	"""

	def __init__(self):
		self.mysql_queries = {
'recent patterns' : {
	'string' : u"""
SELECT pc_username, pc_date, p_path 
	FROM eval_patterns 
		WHERE pc_date > DATE_FORMAT(DATE_SUB(NOW(),INTERVAL 28 DAY),'%s') 
		AND ignored IS NULL;
	""",
	'variables' : True, #this should be a list of string formatting variables, not boolean
	},
'recent endorsements' : {
	'string' : u"""
SELECT rev_user_text, rev_timestamp, p_path 
	FROM eval_pattern_endorsements 
		WHERE rev_timestamp > DATE_FORMAT(DATE_SUB(NOW(),INTERVAL 14 DAY),'%s')
	""",
	'variables' : True,
	},
'recent intros' : {
	'string' : u"""
SELECT rev_user_text, rev_timestamp, p_path 
	FROM eval_profiles 
		WHERE rev_timestamp > DATE_FORMAT(DATE_SUB(NOW(),INTERVAL 14 DAY),'%s') 
		AND ignored IS NULL;""",
	'variables' : True,	
	},
'recent questions' : {
	'string' : u"""
SELECT rev_user_text, rev_timestamp, p_path, rev_comment 
	FROM eval_questions
		WHERE rev_timestamp > DATE_FORMAT(DATE_SUB(NOW(),INTERVAL 7 DAY),'%s');""",
	'variables' : True,	
	},	
'list patterns' : {
	'string' : u"""
SELECT re_date, p_path, page_id 
	FROM eval_patterns 
		WHERE ignored IS NULL and p_namespace = 200;
	""",
	'variables' : False,
	},	
}	
		self.string_variables = { #not using this right now
'rev timestamp' : '%Y%m%d%H%i%s',
	}		

	def getQuery(self, query_type):
		if query_type in self.mysql_queries:
			query_data = self.mysql_queries[query_type]
			if query_data['variables']: #need to abstract
				query = query_data['string'] % (self.string_variables['rev timestamp'])
			else:
				query = query_data['string']	
		else:
			query = "something went wrong"	
			print query
		return query

