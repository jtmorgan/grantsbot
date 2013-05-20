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

class Profiles:
	"""A page on a wiki."""

	def __init__(self, title, namespace = grantsbot_settings.rootpage):
		"""
		Instantiates page-level variables.
		"""
		self.title = title
		self.namespace = namespace
		self.page_path = title + namespace
		self.wiki = wikitools.Wiki(grantsbot_settings.apiurl)

	def getPageText(self, section=False):
		"""
		Gets the raw text of a page or page section.
		Sample: http://meta.wikimedia.org/w/api.php?action=query&prop=revisions&titles=Grants:IdeaLab/Introductions&rvprop=content&rvsection=21&format=jsonfm
		"""
		params = {
			'action': 'query',
			'prop': 'revisions',
			'titles': self.page_path,
			'rvprop' : 'content'
			'rvsection' : section
		}
		req = wikitools.APIRequest(wiki, params)
		response = req.query()
		page_id = response['query']['pages'].keys()[0]
		text = response['query']['pages'][page_id]['revisions'][0]['*']
		return text

	def getPageSectionData(self):
		"""
		Returns the section titles and numbers for a given page.
		Sample request: http://meta.wikimedia.org/w/api.php?action=parse&page=Grants:IdeaLab/Introductions&prop=sections&format=jsonfm
		"""
		params = {
			'action': 'parse',
			'page': self.page_path,
			'prop': 'sections',
		}
		req = wikitools.APIRequest(wiki, params)
		response = req.query()
		secs_list = [{'username' : x['line'], 'profile_index' : x['index']}) for x in response['parse']['sections']]
		return secs_list

	def getUserRecentEdits(self, user_name, edit_namespace):
		"""
		Returns information about a user.
		Currently only gets edits in a given namespace within the past month.
		Sample: http://meta.wikimedia.org/w/api.php?action=query&list=recentchanges&rcnamespace=200&rcuser=Jmorgan_(WMF)&rclimit=500&format=jsonfm
		"""
		params = {
			'action': 'query',
			'list': 'recentchanges',
			'rcuser': user_name,
			'rcnamespace': edit_namespace
		}
		req = wikitools.APIRequest(self.wiki, params) #gets content namespace edits
		response = req.query()
		edits = len(response['query']['recentchanges'])
		return edits

class CategoryMembers:

	def getCategoryMembers(title):
		"""Get the members of a given category and its subcategories."""
		cat_pages = []
		cat_subcats = []
		cat_page = wtcat.Category(wiki, title)
		cat_pages = cat_page.getAllMembers(titleonly=True, namespace=[200,201]) #abstract
		subcat_count = len(cat_page.getAllMembers(titleonly=True, namespace=[14]))
		if len(subcat_count) > 0:

		cat_subcats = cat_page.getAllMembers(titleonly=True, namespace=[200,201])

	def getSubCatPages(cat_subcats):
		for subcat in cat_subcats:
			cat_page = wtcat.Category(wiki, title)

class ProfilePage(Page):
	"""variables and functions related to working with profiles pages."""

class ProposalPage(Page):








