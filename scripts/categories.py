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

	def __init__(self, title, namespace = grantsbot_settings.numeric_namespace, type = "page"):
		"""
		Instantiate basic variables for the category you're interested in.
		"""
		self.cat_title = "Category:" + title
# 		print self.title
		self.mem_type = type
# 		print self.type
		self.mem_namespace = namespace
		self.wiki = wikitools.Wiki(grantsbot_settings.apiurl)
		self.wiki.login(grantsbot_settings.username, grantsbot_settings.password)

	def getCatMembers(self):
		"""
		Get the members of the specified category and their metadata.
		Example: http://meta.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtype=page&cmtitle=Category:IEG/Proposals/IdeaLab&cmnamespace=200&cmprop=title|timestamp|id&cmsort=timestamp&cmdir=desc&format=jsonfm
		"""
		if self.mem_type == 'page':
			query_params = {
			'action': 'query',
			'list': 'categorymembers',
			'cmtitle' : self.cat_title,
			'cmtype': self.mem_type,
			'cmnamespace' : self.mem_namespace,
			'cmprop' : 'title|timestamp|ids',
			'cmsort' : 'timestamp',
			'cmdir' : 'desc'
			}
			req = wikitools.APIRequest(self.wiki, query_params)
			response = req.query()
			mem_list = [{'page_id' : x['pageid'], 'page_path' : x['title'], 'datetime_added' : x['timestamp']} for x in response['query']['categorymembers']]
			return mem_list
		else: print "not set up to get this type of category member yet"


