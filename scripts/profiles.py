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

class Profiles:
	"""A page on a wiki."""

	def __init__(self, title, type, namespace = grantsbot_settings.rootpage):
		"""
		Instantiates page-level variables.
		"""
		self.title = title
# 		print self.title
		self.type = type
# 		print self.type
		self.namespace = namespace
# 		print self.namespace
		self.page_path = namespace + title
# 		print self.page_path
		self.wiki = wikitools.Wiki(grantsbot_settings.apiurl)
		self.wiki.login(grantsbot_settings.username, grantsbot_settings.password)


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
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		secs_list = [{'username' : x['line'], 'profile_index' : x['index']} for x in response['parse']['sections']]
		return secs_list

	def getPageText(self, section=False):
		"""
		Gets the raw text of a page or page section.
		Sample: http://meta.wikimedia.org/w/api.php?action=query&prop=revisions&titles=Grants:IdeaLab/Introductions&rvprop=content&rvsection=21&format=jsonfm
		"""
		params = {
			'action': 'query',
			'prop': 'revisions',
			'titles': self.title,
			'rvprop' : 'content',
			'rvsection' : section
		}
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		page_id = response['query']['pages'].keys()[0]
		text = response['query']['pages'][page_id]['revisions'][0]['*']
		return text

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
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		edits = len(response['query']['recentchanges'])
		return edits

	def getPageInfo(self, val): #need to make this more abstract
		params = {
			'action': 'query',
			'titles': self.title,
			'prop': 'info',
		}
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
# 		print response
		page_id = response['query']['pages'].keys()[0]
		info = response['query']['pages'][page_id][val]
		return info


	def formatProfile(self, val):
		"""
		takes in a dictionary of parameter values and plugs them into the specified template
		"""
		page_templates = templates.Template()
		tmplt = page_templates.getTemplate(self.type)
		tmplt = tmplt.format(**val).encode('utf-8')
# 		print tmplt
		return tmplt

	def publishProfile(self, val, editsumm):
		"""
		Publishes a profile or set of concatenated profiles to a page on a wiki.
		"""
# 		page_templates = templates.Template()
# 		plist_template = page_templates.getTemplate(self.title)
# 		print plist_template.format(**plist_text)
# 		report = plist_template.format(**plist_text).encode('utf-8')
# 		wikipage = wikitools.Page(self.wiki, self.page_path)
		wikipage = wikitools.Page(self.wiki, self.title)
		wikipage.edit(val, summary=editsumm, bot=1) #need to specify the section!