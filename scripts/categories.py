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

# from wikitools import category as wtcat
import wikitools
import grantsbot_settings
import templates

class Categories:
	"""A category on a wiki."""

	def __init__(self, title, type, namespace = grantsbot_settings.numeric_namespace):
		"""
		Instantiates page-level variables.
		"""
		self.title = title
# 		print self.title
		self.type = type
		print self.type
		self.namespace = namespace
# 		print self.namespace
# 		self.page_path = namespace + title
# 		print self.page_path
		self.wiki = wikitools.Wiki(grantsbot_settings.apiurl)
		self.wiki.login(grantsbot_settings.username, grantsbot_settings.password)		
		
	def getCatMembers(self):
		"""
		get the members of the specified category.
		Example: http://meta.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtype=page&cmtitle=Category:IEG/Proposals/IdeaLab&cmnamespace=200&cmprop=title|timestamp&cmsort=timestamp&cmdir=desc&format=jsonfm
		"""
		params = {
		'action': 'query',
		'list': 'categorymembers',
		'cmtitle' : self.title,
		'cmtype': self.type,
		'cmnamespace' : self.namespace, #this needs to be numeric! 200 for grants.
		'cmprop' : 'title|timestamp',
		'cmsort' : 'timestamp',
		'cmdir' : 'desc'
		}
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		mem_list = [{'page_path' : x['title'], 'datetime_added' : x['timestamp']} for x in response['query']['categorymembers']]
		return mem_list		

		
		